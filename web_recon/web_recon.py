# a script to scrape a web site for intersting information

import requests
from bs4 import BeautifulSoup, Comment
import re

# get the url to parse
target_url = input("Enter a target URL (e.g., https://example.com): ")

try:
    response = request.get(target_url, timeout=10)
    # checking HTTP status code
    response.raise_for_status()
    # feed the content to BeautifulSoup to make it searchable
    soup = BeautifulSoup(response.content, "html.parser")

    print(f"\n[+] Successfully breached....er, accessed {target_url}")
    print("---------------------------------------------------------")

    # Hunting for comments
    print("Scanning for careless comments...")
    all_comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    if all_comments:
        print(f"\n[*] Found {len(all_comments)} HTML Comments")
        for comment in all_comments:
            content = comment.strip().lower()
            keywords = ["todo", "fix", "ip", "admin", "pass", "dev", "test"]

            if any(key in content for key in keywords):
                print(f" [!] POTENTIAL LEAD: {comment.strip()}")
            else:
                print(f" [-] Nothing to see here: {comment.strip()}")

    # Hunting for hidden goodies
    print("Scanning for hidden treasures...")
    hidden_fields = soup.find_all("input", type="hidden")

    if hidden_fields:
        print(f"\n[*] Found {len(hidden_fields)} Hidden Form Fields:")
        for field in hidden_fields:
            name = field.get("name", "[No Name]")
            val = field.get("value", "[No Value]")
            print(f" [+] Field: {name} | Value: {val}")

    # Hunting for external links
    print("Scanning for useful links...")
    all_links = [a.get("href") for a in soup.find_all("a", href=True)]
    external = [
        link for link in all_links if target_url not in link and link.startswith("http")
    ]

    # removing duplicates
    unique_external = set(external)
    print(f"\n[*] Found {len(unique_external)} Unique External Links")
    for link in unique_external:
        print(f" [+] Link: {link}")


# adding in the exceptions so the script won't explode...probably
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connection: {errc}")
except Exception as e:
    print(f"An unexpected Error has occurred: {e}")

print("\n[+] Recon Complete. My work here is done.")
