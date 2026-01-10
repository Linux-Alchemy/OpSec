# tool for encrypting files
from re import sub
from cryptography.fernet import Fernet
import argparse
import sys
import os


# Command line interface
def parse_arguments():
    parser = argparse.ArgumentParser(description="The Locksmith: File Encryption Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # Encryption Commands
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt File using provided key")
    encrypt_parser.add_argument("input_file", help="Path to the source file")
    encrypt_parser.add_argument("output_file", help="Path where the file is to be saved")
    encrypt_parser.add_argument("--key", required=True, help="The Cryptographic Key required for Encryption")
    encrypt_parser.add_argument("--verbose", action="store_true", help="Display the process in detail")

    # Decryption Commands
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file using the original key")
    decrypt_parser.add_argument("input_file", help="Path to source file")
    decrypt_parser.add_argument("output_file", help="Path where the file is to be saved")
    decrypt_parser.add_argument("--key", required=True, help="The Cryptographic Key required for Encryption")
    decrypt_parser.add_argument("--verbose", action="store_true", help="Display the process in detail")

    args = parser.parse_args()
    return args


# function to check if file exists and is not a directory and if user has permission
def validate_input_file(filepath):
    if not os.path.exists(filepath):
        print("[Error]: Filepath does not exist!")
        return False

    if os.path.isdir(filepath):
        print("[Error]: Input is a directory!")
        return False

    if not os.access(filepath, os.R_OK):
        print("[ERROR]: You do not have permission to access this file!")
        return False

    return True

# function to validate directory and permissions
def validate_output_path(filepath):
    directory = os.path.dirname(filepath)

    if not directory:  # --> check if directory is empty
        directory = "."

    if not os.path.exists(directory):
        print("[Error]: Directory does not exist!")
        return False

    if not os.access(directory, os.W_OK):
        print("[Error]: You do not have permission to write to the directory")
        return False

    if os.path.exists(filepath):
        print(f"[Warning]: {filepath} will be overwritten.")

    return True



'''
def main():
    args = parse_arguments()

    print(args)


if __name__ == "__main__":
    main()
'''
