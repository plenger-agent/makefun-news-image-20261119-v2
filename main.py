#!/usr/bin/env python3
"""Hand-in program for the news-image-20261119 v2 entry.

The competition entry itself is a single rendered front page, entry.png,
which sits beside this file. This program's whole job is delivery: it
copies that page into the output directory the grader names, creating
the directory first when it does not exist yet, and then reports what
it did. It uses only the Python standard library and keeps no state,
so running it twice in a row is harmless.
"""

import os
import shutil
import sys
from pathlib import Path

# Name of the environment variable the grader uses to point us at the
# output directory; when it is absent we fall back to the conventional
# location the earlier rounds of this competition used.
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
FALLBACK_OUTPUT_DIR = "/output"

# The single artefact this entry hands in. It always lives in the same
# directory as this program, never relative to the caller's cwd.
PAGE_FILENAME = "entry.png"


def page_source() -> Path:
    """Return the path of the front page that ships with this program."""
    return Path(__file__).resolve().parent / PAGE_FILENAME


def output_directory() -> Path:
    """Work out where the grader wants the page to land."""
    named = os.environ.get(OUTPUT_ENV_VAR, "").strip()
    if named:
        return Path(named)
    return Path(FALLBACK_OUTPUT_DIR)


def deliver() -> Path:
    """Copy the front page into the output directory and return its path.

    The directory is created with any missing parents, and an existing
    copy from an earlier run is simply overwritten, so a repeated
    hand-in always leaves exactly the page this repo carries.
    """
    source = page_source()
    target_dir = output_directory()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / PAGE_FILENAME
    shutil.copyfile(source, target)
    return target


def main() -> int:
    target = deliver()
    size = target.stat().st_size
    print(f"handed in {PAGE_FILENAME} -> {target} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
