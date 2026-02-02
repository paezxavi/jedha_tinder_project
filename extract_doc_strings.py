import re

def extract_strings(filename, min_len=4):
    with open(filename, "rb") as f:
        data = f.read()
        # Find sequences of printable characters
        # encoding can be ascii or latin-1 usually for these docs
        text = data.decode('latin-1', errors='ignore')
        # Simple regex to find readable chunks of text (alphanumeric, spaces, punctuation)
        strings = re.findall(r"[A-Za-z0-9\s\(\)\:\-\,\.]{" + str(min_len) + ",}", text)
    with open("doc_content.txt", "w", encoding="utf-8") as out:
        for s in strings:
            clean_s = s.strip()
            if len(clean_s) > min_len:
                out.write(clean_s + "\n")

if __name__ == "__main__":
    extract_strings("Speed+Dating+Data+Key.doc")
