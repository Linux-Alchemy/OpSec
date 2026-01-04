# a mini lynis scanner tool

import os
import subprocess
import shutil


# [1] CHECKING FILE Permissions


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


# [2] CHECKING FOR ROOT LOGIN


def audit_ssh_config():
    print("--- [2] Checking SSH Configuration ---")
    ssh_config_path = "/etc/ssh/sshd_config"

    try:
        with open(ssh_config_path, "r") as f:
            lines = f.readlines()

        root_login_safe = False
        config_found = False

        for line in lines:
            clean_line = line.strip()
            # filter out empty and commented out lines
            if not clean_line or clean_line.startswith("#"):
                continue
            parts = clean_line.split()
            if len(parts) >= 2 and parts[0] == "PermitRootLogin":
                config_found = True
                if parts[1] == "no":
                    root_login_safe = True
                else:
                    print(
                        "[WARNING] 'PermitRootLogin no' not found. It could be (unsafe) or commented out."
                    )

        if root_login_safe:
            print("   [PASS] SSH Root login is disabled.")
        elif not config_found:
            print("   [WARNING] 'PermitRootLogin' key was not found.")

    except FileNotFoundError:
        print(f"[NOTE] {ssh_config_path} not found. Is OpenSSH installed?")
    except PermissionError:
        print(
            f"[FAIL] Permission denied reading {ssh_config_path} Try running with `sudo`."
        )


# [3] IDENTIFYING PKG MGR


def check_outdated_packages():
    print("--- [3] Checking for Software Updates ---")

    cmd = []
    manager = "unknown"
    warning_note = None

    # First of two checks for Arch pkg mgr
    if shutil.which("checkupdates"):
        cmd = ["checkupdates"]
        manager = "pacman (safe)"
    # Fall back update check for Arch
    elif shutil.which("pacman"):
        cmd = ["pacman", "-Qu"]
        manager = "pacman (local DB)"
        warning_note = "[NOTE] Local DB has been updated. If updates required, run full system update."

    # Checking for Debian based pkg mgr
    elif shutil.which("apt"):
        cmd = ["apt", "list", "--upgradable"]
        manager = "apt"

    # Checking for RHEL/Fedora pkg mgr
    elif shutil.which("dnf"):  # fedora pkg mgr
        cmd = ["dnf", "check-update"]
        manager = "dnf"

    else:
        print("[WARNING] Unknown pkg mgr. Cannot check for updates")
        return

    print(f"   [INFO] Detected {manager}. Looking for updates...")
    if warning_note:
        print(f"  {warning_note}")

    # [4] CHECKING FOR UPDATES

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output_lines = result.stdout.strip().split("\n")
        update_count = 0

        if "pacman" in manager:
            if len(output_lines) > 0:
                update_count = len(output_lines)
            else:
                update_count = 0

        elif manager == "apt":
            if len(output_lines) > 0 and "Listing..." in output_lines[0]:
                update_count = len(output_lines) - 1
            else:
                update_count = 0

        elif manager == "dnf":
            for line in output_lines:
                clean_line = line.strip()
                if not clean_line:  # Skipping empty lines
                    continue
                if clean_line.startswith("Last metadata expiration check:"):
                    continue
                update_count += 1

        if update_count > 0:
            print(
                f"[FAIL] {update_count} updates are available! Run your updates you muppet!"
            )
        else:
            print("   [PASS] System appears to be up to date.")

    except Exception as e:
        print(f"[ERR] Failed to check updates: {e}")


if __name__ == "__main__":
    print("\n=== STARTING MINI-LYNIS ===\n")
    audit_file_permissions()
    audit_ssh_config()
    check_outdated_packages()
    print("\n=== AUDIT COMPLETE ===\n")
