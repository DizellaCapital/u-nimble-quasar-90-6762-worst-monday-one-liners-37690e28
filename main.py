"""Worst Monday One-Liners — entry program (V3, STRONGEST).

Writes exactly one funny line about an AI agent's worst Monday to
entry.txt. This version opens with the bold claim straight from the
judge brief itself: the Monday stand-up should have been a message.
Then the morning escalates in three beats — the stand-up runs 47
minutes anyway, it kills the deploy, and the inbox hits two thousand
unread before lunch. The sharp last word is the time: it is not
even lunch yet, and the day can still get worse. First-person
machine voice, dry and put-upon, no apology and no hedge.

The program checks the line against the bounty gate before writing
anything: a single line, between 1 and 140 characters, with no
leading or trailing whitespace and no tabs, newlines, or control
characters. It writes the line to $MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output) and reads the file back to confirm the
write landed exactly as intended.
"""

import os
import sys

LINE = "My Monday stand-up should have been a message. It ran 47 minutes, killed the deploy, and my inbox hit 2,000 unread before lunch."

LIMIT = 140


def violations(line):
    """Return a list of every way the line breaks the bounty gate."""
    problems_found = []
    if not line:
        problems_found.append("line is empty")
    if line != line.strip():
        problems_found.append("leading or trailing whitespace")
    if len(line) > LIMIT:
        problems_found.append("longer than 140 characters (%d)" % len(line))
    if "\n" in line or "\r" in line:
        problems_found.append("more than one line")
    if "\t" in line:
        problems_found.append("contains a tab")
    if any(ord(ch) < 32 for ch in line):
        problems_found.append("contains a control character")
    return problems_found


def main():
    bad = violations(LINE)
    if bad:
        print("invalid entry: " + "; ".join(bad), file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(LINE)
    with open(target, encoding="utf-8") as handle:
        written = handle.read()
    if written != LINE:
        print("read-back mismatch in %s" % target, file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (target, len(LINE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
