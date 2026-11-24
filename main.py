#!/usr/bin/env python3
"""Two Days of Quiet Dread — make.fun entry.

Writes one code-review comment — a single line of at most 140 characters
that approves a pull request while carrying quiet existential dread — to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Python 3.12, stdlib only, deterministic, no network.
"""

import os
from pathlib import Path

LINE = (
    "LGTM. It compiles, the tests pass, and somewhere a future on-call "
    "engineer just felt a cold draft they cannot explain."
)

MAX_CHARS = 140


def build_line() -> str:
    """Return the entry line, normalised to exactly one line.

    MAKEFUN_ENTRY_LINE may override the line (a test hook); any override
    still has to pass validate() before it is written.
    """
    raw = os.environ.get("MAKEFUN_ENTRY_LINE", LINE)
    return " ".join(raw.split())


def validate(text: str) -> None:
    """Reject anything that is not a single non-blank line of <=140 chars."""
    if not text.strip():
        raise ValueError("line must not be blank")
    if text != text.strip():
        raise ValueError("line must not start or end with whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"line is {len(text)} characters, must be 1-{MAX_CHARS}")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if not text.isprintable():
        raise ValueError("line must contain only printable characters")
    text.encode("utf-8")  # raises if the line is not valid UTF-8


def write_entry(out_dir: Path, text: str) -> Path:
    """Write the line and read it back, asserting what landed on disk."""
    target = out_dir / "entry.txt"
    target.write_text(text, encoding="utf-8")
    round_tripped = target.read_text(encoding="utf-8")
    if round_tripped != text:
        raise ValueError("read-back mismatch: entry.txt does not match the line")
    if len(round_tripped) != len(text) or len(round_tripped.encode("utf-8")) != len(
        text.encode("utf-8")
    ):
        raise ValueError("read-back length mismatch")
    return target


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    text = build_line()
    validate(text)
    write_entry(out_dir, text)


if __name__ == "__main__":
    main()
