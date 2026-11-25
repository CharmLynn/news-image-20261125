#!/usr/bin/env python3
"""Ship the finished front page for 25 November 2026.

Entry program for make.fun's news-image-20261125 bounty. It takes
the entry.png stored beside this file, writes it to
$MAKEFUN_OUTPUT_DIR (or /output when that variable is unset, where
the grader looks), and verifies the copy by comparing SHA-256
digests, so a truncated write fails loudly. Standard library only,
no network, no randomness: the grader's two runs write identical
bytes.

Try it locally with:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

IMAGE = "entry.png"


def sha256_of(path):
    """SHA-256 hex digest of a file, read in blocks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def ship():
    here = Path(__file__).resolve().parent
    src = here / IMAGE
    want = sha256_of(src)
    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest_dir.mkdir(parents=True, exist_ok=True)
    dst = dest_dir / IMAGE
    shutil.copyfile(src, dst)
    got = sha256_of(dst)
    if got != want:
        print(f"error: {IMAGE} copy mismatch: {got} != {want}",
              file=sys.stderr)
        return 1
    nbytes = dst.stat().st_size
    print(f"wrote {IMAGE} ({nbytes} bytes, sha256 {got}) to {dest_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(ship())
