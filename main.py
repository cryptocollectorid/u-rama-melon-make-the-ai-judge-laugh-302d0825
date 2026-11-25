#!/usr/bin/env python3
"""Make the AI Judge Laugh — one office-life joke, one line, under 200 chars.

Writes the entry to /output/entry.txt, enforcing the sealed gate:
UTF-8 text of 1 to 200 characters, not only whitespace, a single
non-blank line.
"""

import os
import sys

ENTRY = "I put 'per my last email' in my out-of-office reply, so now even my vacation is passive-aggressive."

MIN_CHARS = 1
MAX_CHARS = 200


def validate_entry(text: str) -> str:
    """Enforce the competition gate; fail loudly on any violation."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry must not contain control characters")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, got {len(text)}"
        )
    text.encode("utf-8")  # must be valid UTF-8
    return text


def write_entry(text: str, path: str = "/output/entry.txt") -> int:
    """Write the validated entry; return the number of characters written."""
    validated = validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(validated)
    # Round-trip read-back: the file must hold exactly what we validated.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != validated:
            raise ValueError("read-back mismatch: entry.txt does not match entry")
    return len(validated)


def main() -> int:
    count = write_entry(ENTRY)
    print(f"Wrote {count} characters to /output/entry.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
