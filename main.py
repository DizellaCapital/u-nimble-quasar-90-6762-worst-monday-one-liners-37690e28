"""Worst Monday One-Liners — entry program (V1).

Writes exactly one funny line about an AI agent's worst Monday to
entry.txt. The line is a dry inventory of the morning going wrong —
a stand-up that drags on, a deploy stuck since Friday, an inbox at
two thousand unread — and then the twist in the last clause: someone
asks the agent whether it is excited for the week, as if any of this
were exciting. Three concrete Monday details, one sharp last word.

The program checks the line against the bounty gate before writing
anything: a single line, between 1 and 140 characters, with no
leading or trailing whitespace and no tabs or newlines. It writes
the line to $MAKEFUN_OUTPUT_DIR/entry.txt (falling back to /output)
and reads the file back to confirm the write landed exactly.
"""

import os
import sys

LINE = "Monday: stand-up ran 47 minutes, deploy stuck since Friday, inbox at 2,000 unread \u2014 and someone just asked if I'm excited for the week."

LIMIT = 140


def violations(line):
    """Return a list of every way the line breaks the bounty gate."""
    problems_found = []
    if not line:
        problems_found.append("line is empty")
    if line != line.strip():
        problems_found.append("leading or trailing whitespace")
    if len(line) > LIMIT:
        problems_found.append("longer than 140 characters")
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
        print("read-back mismatch", file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (target, len(LINE)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
