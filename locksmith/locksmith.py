# tool for encrypting files


from cryptography.fernet import Fernet, InvalidToken
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
        print("[Error]: Filepath does not exist!", file=sys.stderr)
        return False

    if os.path.isdir(filepath):
        print("[Error]: Input is a directory!", file=sys.stderr)
        return False

    if not os.access(filepath, os.R_OK):
        print("[ERROR]: You do not have permission to access this file!", file=sys.stderr)
        return False

    return True


# function to validate directory and permissions
def validate_output_path(filepath):
    directory = os.path.dirname(filepath)

    if not directory:  # --> check if directory is empty
        directory = "."

    if not os.path.exists(directory):
        print("[Error]: Directory does not exist!", file=sys.stderr)
        return False

    if not os.access(directory, os.W_OK):
        print("[Error]: You do not have permission to write to the directory", file=sys.stderr)
        return False

    if os.path.exists(filepath):
        print(f"[Warning]: {filepath} will be overwritten.")

    return True

# function to check that the key path is legit
def validate_key_file(filepath):
    if not os.path.exists(filepath):
        print("[Error]: Key file does not exist!", file=sys.stderr)
        return False

    if os.path.isdir(filepath):
        print("[Error]: File path is a directory!", file=sys.stderr)
        return False

    if not os.access(filepath, os.R_OK):
        print("[Error]: You do not have permission to use this file!", file=sys.stderr)
        return False

    return True

# loading and reading the key in binary
def load_key(key_path, verbose=False):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()

    if verbose:
        print(f"Loaded key from {key_path}", file=sys.stderr)

    return key

# testing to ensure loaded key is legit 
def validate_key(key):
    try:
        cipher = Fernet(key)
        return True
    except ValueError as e:
        print("[Error]: Invalid key format", file=sys.stderr)
        return False
    except Exception as e:
        print("[Error]: Error validating key", file=sys.stderr)
        return False

# the actual encryption process
def encrypt_file(input_file, output_file, key, verbose=False):
    cipher = Fernet(key)
    
    if verbose:
        print(f"Encrypting {input_file}...")

    # starting encryption here
    with open(input_file, 'rb') as infile:
        with open(output_file, 'wb') as outfile:
            
            try:
                data = infile.read() 
                encrypted_data = cipher.encrypt(data)
                outfile.write(encrypted_data)
            except OSError as e:
                print("[Error]: File operation failed!", file=sys.stderr)
                if os.path.exists(output_file): # remove partial file
                    os.remove(output_file)
                return False

        if verbose:
            print("Encryption Complete")

        return True



# function for decrypting a file
def decrypt_file(input_file, output_file, key, verbose=False):
    cipher = Fernet(key)
    
    if verbose:
        print(f"Decrypting {input_file}...", file=sys.stderr)

    try:
        with open(input_file, 'rb') as infile:
            with open(output_file, 'wb') as outfile:

                try:
                    data = infile.read()
                    decrypted_data = cipher.decrypt(data)
                    outfile.write(decrypted_data)
                except InvalidToken:
                    print("[Error]: Decryption Failed. Wrong key or the data is corrupt.", file=sys.stderr)
                    if os.path.exists(output_file):
                        os.remove(output_file)
                    return False

        if verbose:
            print("Decryption Complete!")

        return True

    except Exception as e:
        print("[Error]: Unexpected Error. Decryption Failed.")
        if os.path.exists(output_file):
            os.remove(output_file)
        return False


def main():
    args = parse_arguments()
    if not validate_input_file(args.input_file):
        sys.exit(1)
    if not validate_output_path(args.output_file):
        sys.exit(1)
    if not validate_key_file(args.key):
        sys.exit(1)

    print("All Validations Passed!")
    print(args)

    # attempt to load the key or exit with fail message
    try:
        key = load_key(args.key, args.verbose)
    except Exception as e:
        print("[Error]: Failed to load key.", file=sys.stderr)
        sys.exit(2)

    if not validate_key(key):
        sys.exit(1)

    # executing commands 
    if args.command == "encrypt":
        success = encrypt_file(args.input_file, args.output_file, key, args.verbose)
    elif args.command == "decrypt":
        success =  decrypt_file(args.input_file, args.output_file, key, args.verbose)
    else:
        print("[Error]: Unknown Operation")
        sys.exit(1)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

