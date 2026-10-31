import argparse
import logging
import pandas as pd
import sys
import os  # For accessing environment variables


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Detects reverse shell connections by analyzing network traffic data."
    )

    parser.add_argument(
        "-i",
        "--input",
        dest="input_file",
        required=True,
        help="Path to the network traffic data file (e.g., CSV, PCAP converted to CSV).",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        default="reverse_shell_report.txt",
        help="Path to save the analysis report. Defaults to reverse_shell_report.txt",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        dest="threshold",
        type=float,
        default=0.8,
        help="Threshold for flagging suspicious connections (e.g., communication frequency, data transfer).  A higher value means fewer false positives, but a greater risk of missing actual shells. Defaults to 0.8.",
    )
    parser.add_argument(
        "--min-bytes",
        dest="min_bytes",
        type=int,
        default=1000000,
        help="Minimum total bytes a connection group must reach before the relative score alone can flag it. Defaults to 1000000 (1 MB). A group can also be flagged on its absolute score alone, which is computed from total bytes only.",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="format",
        default="csv",
        choices=["csv"],
        help="Format of the input file. Only 'csv' is supported. Defaults to 'csv'.",
    )

    return parser


def load_data(input_file, file_format):
    """
    Loads network traffic data from the specified file.

    Args:
        input_file (str): Path to the input file.
        file_format (str): Format of the input file (e.g., "csv").

    Returns:
        pandas.DataFrame: DataFrame containing the network traffic data.
        Returns None if an error occurs.
    """
    try:
        if file_format == "csv":
            # Securely read the CSV file
            df = pd.read_csv(input_file, low_memory=False)  # low_memory=False for large files
            logging.info(f"Successfully loaded data from {input_file}")
            return df
        else:
            logging.error(f"Invalid file format: {file_format}")
            print("Error: Invalid file format.")
            return None
    except FileNotFoundError:
        logging.error(f"Input file not found: {input_file}")
        print(f"Error: Input file not found: {input_file}")  # Informative message to the user
        return None
    except pd.errors.ParserError:
        logging.error(f"Error parsing the CSV file: {input_file}.  Check the file format and delimiters.")
        print(f"Error: Error parsing the CSV file: {input_file}.  Check the file format and delimiters.")  # User-friendly message
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading data: {e}")
        print(f"An unexpected error occurred: {e}")  # User-friendly message
        return None


ABSOLUTE_SCALE_BYTES = 100000000


def analyze_network_traffic(df, threshold, min_bytes=1000000):
    """
    Analyzes network traffic data to detect potential reverse shell connections.

    Args:
        df (pandas.DataFrame): DataFrame containing network traffic data.
        threshold (float): Threshold for flagging suspicious connections.

    Returns:
        pandas.DataFrame: DataFrame containing suspicious connections.
    """
    try:
        # Input validation
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a Pandas DataFrame.")
        if not isinstance(threshold, (int, float)):
            raise ValueError("Threshold must be a number.")
        if threshold < 0 or threshold > 1:
            raise ValueError("Threshold must be between 0 and 1.")

        # Basic example: Analyze communication frequency and data transfer characteristics.
        # Replace this with more sophisticated analysis based on your specific data.
        # Ensure proper column names exist in the dataframe.
        if 'source_ip' not in df.columns or 'destination_ip' not in df.columns or 'bytes_sent' not in df.columns or 'packets_sent' not in df.columns:
            logging.error("Required columns ('source_ip', 'destination_ip', 'bytes_sent', 'packets_sent') are missing from the input data.")
            print("Error: Required columns ('source_ip', 'destination_ip', 'bytes_sent', 'packets_sent') are missing from the input data.")
            # None, not an empty frame: an empty frame means "ran fine, found
            # nothing", and the caller exits 1 on None. Returning empty here
            # used to print a clean report for input that was never analysed.
            return None
        if df.empty:
            logging.error("Input data has no rows to analyse.")
            print("Error: Input data has no rows to analyse.")
            return None

        # Group by source and destination IP, calculate total bytes and packets sent
        connection_stats = df.groupby(['source_ip', 'destination_ip']).agg(
            total_bytes=('bytes_sent', 'sum'),
            total_packets=('packets_sent', 'sum'),
            connection_count=('source_ip', 'size')
        ).reset_index()

        # Calculate an "anomaly score" based on bytes transferred and packet count
        # This is a simplified example; improve this based on real-world traffic patterns
        connection_stats['anomaly_score'] = (connection_stats['total_bytes'] * connection_stats['total_packets']) / connection_stats['connection_count']

        # Normalize the anomaly score between 0 and 1 using min-max scaling.
        # This normalized score is relative to this input file only, so it
        # is kept as supporting detail and never flags a group on its own.
        min_score = connection_stats['anomaly_score'].min()
        max_score = connection_stats['anomaly_score'].max()
        if max_score - min_score != 0:  # Avoid division by zero if all scores are the same
            connection_stats['normalized_score'] = (connection_stats['anomaly_score'] - min_score) / (max_score - min_score)
        else:
            connection_stats['normalized_score'] = 0.0  # All scores are the same, so normalize to 0.0

        # Absolute score from total bytes alone, on a fixed scale:
        # a group at ABSOLUTE_SCALE_BYTES scores 0.5, and the score
        # approaches 1.0 as the transfer grows past that scale. This
        # lets a single large group be flagged, which the relative
        # score alone could never do.
        connection_stats['absolute_score'] = connection_stats['total_bytes'] / (connection_stats['total_bytes'] + ABSOLUTE_SCALE_BYTES)

        # Flag a group when its absolute score exceeds the threshold,
        # or when its relative score exceeds the threshold and the
        # group also transferred at least min_bytes in total. A small
        # group is therefore not flagged on relativity alone.
        suspicious_connections = connection_stats[
            (connection_stats['absolute_score'] > threshold)
            | ((connection_stats['normalized_score'] > threshold) & (connection_stats['total_bytes'] >= min_bytes))
        ]

        logging.info(f"Analysis complete. Found {len(suspicious_connections)} suspicious connections based on the threshold.")
        return suspicious_connections
    except ValueError as ve:
        logging.error(f"ValueError during analysis: {ve}")
        print(f"Error: {ve}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during analysis: {e}")
        print(f"An unexpected error occurred during analysis: {e}")
        return None


def generate_report(suspicious_connections, output_file, threshold, min_bytes=1000000):
    """
    Generates a report of suspicious connections and saves it to a file.

    Args:
        suspicious_connections (pandas.DataFrame): DataFrame containing suspicious connections.
        output_file (str): Path to the output file.
        threshold (float): The threshold used for the analysis.
    """
    try:
        # Input validation
        if not isinstance(suspicious_connections, pd.DataFrame):
            raise ValueError("Suspicious connections must be a Pandas DataFrame.")
        if not isinstance(output_file, str):
            raise ValueError("Output file must be a string.")

        with open(output_file, "w") as f:
            f.write("Reverse Shell Detection Report\n")
            f.write("-------------------------------\n")
            f.write(f"Analysis Threshold: {threshold}\n")
            f.write(f"Minimum Bytes for a Relative Score Flag: {min_bytes}\n")
            f.write("Scoring: each connection group gets an absolute score from its total bytes alone (total_bytes / (total_bytes + 100000000)) and a relative normalized score computed within this input file. A group is flagged when its absolute score exceeds the threshold, or when its relative score exceeds the threshold and its total bytes reach the minimum bytes value. The relative score alone never flags a group below that minimum.\n")
            f.write("-------------------------------\n\n")

            if suspicious_connections.empty:
                f.write("No suspicious connections found above the threshold.\n")
                logging.info("No suspicious connections found, report written.")
            else:
                f.write("Suspicious Connections:\n\n")
                f.write(suspicious_connections.to_string())  # Write the DataFrame to the file
                f.write("\n\n")
                logging.info(f"Suspicious connections found. Report written to {output_file}")

        return True
    except IOError as ioe:
        logging.error(f"IOError while writing the report: {ioe}")
        print(f"Error: Could not write report to {output_file}: {ioe}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred while generating the report: {e}")
        print(f"An unexpected error occurred while generating the report: {e}")
        return False


def main():
    """
    Main function to execute the reverse shell detector.
    """
    try:
        parser = setup_argparse()
        args = parser.parse_args()

        # Validate input arguments
        if not os.path.exists(args.input_file):
            logging.error(f"Input file not found: {args.input_file}")
            print(f"Error: Input file not found: {args.input_file}")  # Informative message to the user
            sys.exit(1)

        if not 0 <= args.threshold <= 1:
            logging.error("Threshold must be between 0 and 1.")
            print("Error: Threshold must be between 0 and 1.")  # Informative message to the user
            sys.exit(1)

        # Load data
        df = load_data(args.input_file, args.format)
        if df is None:
            sys.exit(1)  # Exit if data loading failed

        # Analyze network traffic
        suspicious_connections = analyze_network_traffic(df, args.threshold, args.min_bytes)
        if suspicious_connections is None:
            sys.exit(1)

        # Generate report. The saved message is printed only when the write
        # actually happened; it used to print even after an IOError.
        if not generate_report(suspicious_connections, args.output_file, args.threshold, args.min_bytes):
            sys.exit(1)

        print(f"Analysis complete. Report saved to {args.output_file}")
        logging.info("Reverse shell detector completed successfully.")

    except Exception as e:
        logging.critical(f"An unhandled error occurred: {e}")
        print(f"A critical error occurred: {e}")  # Inform the user of a critical error
        sys.exit(1) # Ensure the program exits with an error status


if __name__ == "__main__":
    main()
