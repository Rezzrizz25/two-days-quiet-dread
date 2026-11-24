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


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    text = LINE.strip()
    if not 1 <= len(text) <= 140:
        raise ValueError(f"line is {len(text)} characters, must be 1-140")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    if not text.strip():
        raise ValueError("line must not be blank")
    (out_dir / "entry.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
