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


# temp testing line
if __name__ == "__main__":
    audit_file_permissions()
