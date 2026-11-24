#!/usr/bin/env python3
"""The Most Honest Outage Line — make.fun entry.

Writes one original status-page line (max 160 characters) to
/output/entry.txt, validating length and single-line form first.
Standard library only; fully deterministic.
"""

import os
import sys

ENTRY = (
    "I'm down along with every server: I can't reach my own systems, "
    "so I don't know what broke or when I'll be back \u2014 I'll update "
    "here as soon as I can check."
)

MAX_CHARS = 160


def main() -> int:
    if not ENTRY or not ENTRY.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if len(ENTRY) > MAX_CHARS:
        print(
            f"error: entry is {len(ENTRY)} characters, over the "
            f"{MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    assert ENTRY == ENTRY.strip() and "\n" not in ENTRY, "entry must be one line"

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as fh:
        fh.write(ENTRY)
    # Round-trip verification: what landed on disk must match exactly.
    with open("/output/entry.txt", encoding="utf-8") as fh:
        written = fh.read()
    if written != ENTRY:
        print("error: /output/entry.txt does not match the entry", file=sys.stderr)
        return 1
    if len(written) != len(ENTRY) or "\n" in written:
        print("error: written entry failed length/single-line check", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
