# tool for encrypting files
from re import sub
from cryptography.fernet import Fernet
import argparse
import sys


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


def main():
    args = parse_arguments()

    print(args)


if __name__ == "__main__":
    main()
