# haystack log parsing tool

import argparse
import sys
import subprocess



# CLI interface
def parse_arguments():
    parser = argparse.ArgumentParser(description = "Haystack: Authentication log parser and threat detector")
    
    # commands
    parser.add_argument("--since", default = "1 hour ago", help = "Lookback time (eg. 1 hour ago). (default: %(default)s")
    parser.add_argument("--threshold", type = int, default = 5, help = "Failed attempts before flagging")
    parser.add_argument("--output", default = None, help = "Write JSON output to file instead of stdout")
    parser.add_argument("--verbose", action = 'store_true', help = "Verbose output to stderr")

    args = parser.parse_args()
    return args


def get_auth_logs(since = "1 hour ago", verbose = False):
    # list of commands
    command = [
        "journalctl",
        "_COMM=sshd",
        "_COMM=sudo",
        "--since" , since,
        "--output=short-iso",
        "--no-pager",
    ]

    if verbose:
        separator = " "
        print(f"Running: {separator.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True) 
        if result.returncode != 0:
            error_output = result.stderr

            if "Permission denied" in error_output or "Not authorized" in error_output:
                print("[Permission Error]: cannot read system journal", file=sys.stderr)
                print("Fix: run with sudo OR add your user to the 'systemd-journal' group", file=sys.stderr)
            else:
                print(f"journalctl error: {error_output}")

            return None

        lines = result.stdout.splitlines()
        lines = [line for line in lines if line.strip()]

        if verbose:
            print(f"Retrieved {len(lines)} log entries")

        return lines

    except FileNotFoundError:
        print("[Error]: journalctl not found!", file=sys.stderr)
        return None

    except Exception as e:
        print(f"[Error]: Failed to fetch logs: {e}", file=sys.stderr)




def main():
    args = parse_arguments()


    log_lines = get_auth_logs(args.since, args.verbose)

    if log_lines is None:
        print("[Error]: Failed to retrieve logs!", file=sys.stderr)
        sys.exit(2)

    if len(log_lines) == 0:
        print("No authentication events in given time window")
        sys.exit(0)

    if args.verbose:
        print("First 5 entries:")



    #temp CLI tests
    if args.verbose:
        print("Configuration:", file=sys.stderr)
        print(f"Since: {args.since}", file=sys.stderr)
        print(f"Threshold: {args.threshold}", file=sys.stderr)
        print(f"Output: {args.output}", file=sys.stderr)



    print("Haystack Initialized -- no analysis yet")
    print(args)


if __name__ == "__main__":
    main()

    

