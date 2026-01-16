# haystack log parsing tool

import argparse
import sys
from datetime import timedelta
from durations import Duration


# function to parse the lookback duration and convert to ISO-timestamp
def parse_duration(string: str):
    try:
        return Duration(string).to_timedelta()
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))

# CLI interface
def parse_arguments():
    parser = argparse.ArgumentParser(description = "Haystack: Authentication log parser and threat detector")
    subparsers = parser.add_subparsers(dest = "command", help = "Available sub-commands")

    # sub-commands
    scan = subparsers.add_parser("haystack", help = "Begin the scanning process")
    scan.add_argument("--since", type = parse_duration, default = "1h", help = "Lookback time (eg. 1h, 1d, 30m, 90s). (default: %(default)")
    scan.add_argument("--threshold", type = int, default = 5, help = "Failed attempts before flagging")
    scan.add_argument("--output", default = None, help = "Write JSON output to file instead of stdout")
    scan.add_argument("--verbose", action = 'store_true', help = "Verbose output to stderr")

    args = parser.parse_args()
    return args

    
    

