## Goal
A lightweight riff on the well known Lynis scanner. This is a very simplified version just to test out the use of the python libraries. It looks for just a few things like writable files that shouldn't be, SSH mis-configs and out of date packages.
---
## How to use
- **Step 1:** Grab the script
- **Step 2:** Make it executable
```bash
chmod +x mini_lynis.py
- **Step 3:** Run it. You'll likely need `sudo` to see the sensitive stuff.
---
## Notes
- **Permissions:** You need to run this with `sudo`. If not it'll complain that it can't read `/etc/shadow` which is a good thing, but not really helpful for the scanner.
- **Compatability:** It attempts to detect `pacman`, `apt` or `dnf`. If you're running something else, you're on your own. 
- **Attitude:** If it finds out of date packages, it'll call you a muppet. Don't take it personally, just update your system.
---

```
```
