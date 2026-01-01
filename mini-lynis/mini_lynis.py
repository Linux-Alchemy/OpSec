# a mini lynis scanner tool

import os

# Pass or Fail functions
"""
def print_success(message):
    <code here>
        pass

def print_fail(message):
    <code here>
        pass
"""


def audit_file_permissions():
    print("--- [1] Checking File Permissions ---")

    sensitive_files = [
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/hosts",
    ]

    issues_found = []

    for filepath in sensitive_files:
        try:
            file_stat = os.stat(filepath)
            if file_stat.st_mode & 0o002:
                issues_found.append(f"[FAIL] {filepath} is World-Writable!")
            else:
                pass

        except FileNotFoundError:
            print(
                f"[NOTE] {filepath} not found. That's alarming. Skipping, but you should probably look into that."
            )
        except PermissionError:
            print(f"[WARN] Could not read permissions for {filepath}. Run as `sudo`.")

    if issues_found:
        for issue in issues_found:
            print(issue)
    else:
        print("   [Pass] No file permission issues found.")


def audit_ssh_config():
    print("--- [2] Checking SSH Configuration ---")
    ssh_config_path = "/etc/ssh/sshd_config"

    try:
        with open(ssh_config_path, "r") as f:
            lines = f.readlines()

        root_login_safe = False

        for line in lines:
            clean_line = line.strip()
            # filter out empty and commented out lines
            if not clean_line or clean_line.startswith("#"):
                continue
            parts = clean_line.split()
            if len(parts) >= 2 and parts[0] == "PermitRootLogin":
                if parts[1] == "no":
                    root_login_safe = True
                else:
                    print(
                        "[WARNING] 'PermitRootLogin no' not found. It could be (unsafe) or commented out."
                    )

    except FileExistsError:
        print(f"[NOTE] {ssh_config_path} not found. Is OpenSSH installed?")
    except PermissionError:
        print(
            f"[FAIL] Permission denied reading {ssh_config_path} Try running with `sudo`."
        )
