# tool for encrypting files
from cryptography.fernet import Fernet


def generate_key(file_path):
    key = Fernet.generate_key()
    with open(file_path, "wb") as file:
        file.write(key)


def load_key(file_path):
    with open(file_path, "rb") as file:
        key = file.read()
        return key


def main():
    print("========LockMaster Encryption Tool========")
    print("Select an option from the menu:")
    options = ["[1] Generate Key", "[2] Encrypt", "[3] Decrypt", "[4] Exit"]
    print(*options, sep="\n")

    while True:
        try:
            choice = int(input("Select an option from the menu (eg, 1, 2, 3, 4): "))
            if choice == 1:
                generate_key("super_secret.key")
            elif choice == 2:
                print("placeholder 2")
            elif choice == 3:
                print("placeholder 3")
            elif choice == 4:
                print("goodbye")
                break
            else:
                print("It would be a lot better if you made a valid selection.")
        except ValueError:
            print("Invalid entry, try again.")


if __name__ == "__main__":
    main()
