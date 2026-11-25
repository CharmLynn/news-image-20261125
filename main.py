#!/usr/bin/env python3
"""Ship the finished front page for 25 November 2026.

Entry program for make.fun's news-image-20261125 bounty. It copies
the entry.png stored next to this file into $MAKEFUN_OUTPUT_DIR
(or /output when that variable is unset, which is where the grader
looks), then compares the copy's SHA-256 digest with the original
so a truncated or corrupted write fails loudly. Standard library
only, no network, no randomness: the grader's two runs write
identical bytes.

Try it locally with:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

IMAGE = "entry.png"


def digest(path):
    """SHA-256 hex digest of a file, read in blocks."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main():
    here = Path(__file__).resolve().parent
    source = here / IMAGE
    expected = digest(source)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / IMAGE
    shutil.copyfile(source, target)
    actual = digest(target)
    if actual != expected:
        print(f"error: {IMAGE} copy mismatch: {actual} != {expected}",
              file=sys.stderr)
        return 1
    size = target.stat().st_size
    print(f"wrote {IMAGE} ({size} bytes, sha256 {actual}) to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
