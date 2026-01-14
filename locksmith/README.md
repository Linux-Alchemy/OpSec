## Goal

An exploration into the dark arts of encryption and a fully workable CLI-based tool. It's designed for those moments when you realize that leaving your "Super Secret Plans for Galactic Domination" in a plain text file is, quite frankly, a bit shit.

## How to use
- **Step 1:** Ensure you have the `cryptography` library installed, along with its various hangers-on.
- **Step 2:** Make the script executable
```bash
chmod +x locksmith.py
- **Step 3:** Run the command with youre `input`, `output`, and a `key file`, preferrably one that exists.
```bash
./locksmith.pyt encrypt sensitive_stuff.txt secrets.enc --key mykey.key
```

## Notes

- **Dependencies:** This requires Python 3 and the `cryptography` library.
- **Validation:** This script checks if files exist, if you’re trying to encrypt a directory (don't), and if you actually have the permissions to touch the files in the first place.
- **The Key:** The tool expects a path to a file containing a valid Fernet key. If you provide a corrupted key or a file full of nonsense, it will politely tell you to bugger off and try again.


```
```
