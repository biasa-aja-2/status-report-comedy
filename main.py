#!/usr/bin/env python3
"""Status Report Comedy Sprint — one funny status-report line, to /output/entry.txt.

The line is assembled from three parts so each beat of the joke stays
visible in the source:

  * the setup — a weekly report, and the agent's context window running
    almost full, which is a real, everyday agent problem;
  * the coping move — the agent summarises its own summary to make room,
    cheerfully obedient as always, exactly the kind of thing an agent
    does when its context window fills up mid-week;
  * the punchline — the summary ate the week itself, and now neither the
    agent nor its human knows what Tuesday was for.

Then the finished line is run through the competition's gates (UTF-8,
1-200 characters, exactly one line, not whitespace-only, no control
characters) and only written out if every gate passes. The program writes
no trailing newline, so the file holds exactly the line and nothing else.

Pure standard library: os and sys only.
"""

import os
import sys

MAX_CHARS = 200

# The three beats of the status report, joined with spaces.
OPENING = "Weekly report: my context window hit 96%,"
EVIDENCE = "so I summarised my own summary,"
PUNCHLINE = "and now neither of us knows what I actually did on Tuesday."


def assemble_line() -> str:
    """Join the report's beats into its single line."""
    return " ".join((OPENING, EVIDENCE, PUNCHLINE))


def gate_problems(line: str) -> list[str]:
    """Return every gate the line fails, or an empty list when it passes."""
    problems: list[str] = []
    if not line:
        problems.append("line is empty")
    if not line.strip():
        problems.append("line is whitespace-only")
    if len(line) > MAX_CHARS:
        problems.append(f"line is {len(line)} characters, over the {MAX_CHARS} limit")
    if "\n" in line or "\r" in line:
        problems.append("line spans more than one line")
    for char in line:
        if ord(char) < 0x20 and char not in ("\t",):
            problems.append(f"line holds a control character U+{ord(char):04X}")
            break
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"line is not encodable as UTF-8: {exc}")
    return problems


def output_path() -> str:
    """Where the line goes: MAKEFUN_OUTPUT_DIR, else /output."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(directory, "entry.txt")


def main() -> int:
    line = assemble_line()
    problems = gate_problems(line)
    if problems:
        for problem in problems:
            print(f"gate failed: {problem}", file=sys.stderr)
        return 1

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)

    # Read it back and confirm the file holds exactly the line.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        print("verification failed: file does not match the line", file=sys.stderr)
        return 1

    print(f"wrote {len(line)}-character status report to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
