#!/usr/bin/env python3
"""make.fun entry for news-image-20261119: "Sum up 19 November's world news in one image".

The repository holds the front-page image as entry.png (a 1024x1024 PNG,
666,996 bytes): "The World in One Day — Thursday 19 November 2026" -
a dated broadsheet front page of that day's real world news: a big-number
stat strip, 13 drawn story cards (the Shenzhen Trump-Xi-Putin summit, GTA
VI's launch day, Anthropic's record IPO, the ICJ Rohingya judgment, Cyclone
Akvan, COP31's final hours and more), a dot-matrix world map with the 13
stories pinned, 23 further one-line briefs, and a DATE CHECK box naming the
stories left out because they were first reported on 18 November. This
program copies that image, byte for byte, to the output location. It uses
only the Python standard library, needs no network, and is deterministic:
every run writes exactly the same bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_IMAGE = HERE / "entry.png"


def output_path() -> Path:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / "entry.png"


def main() -> None:
    # Self-check the asset against the competition gate before copying:
    # a whole PNG (signature plus IEND trailer) of at most 1 MiB.
    data = SOURCE_IMAGE.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n"), "entry.png is not a PNG"
    assert data.rstrip().endswith(b"IEND\xaeB`\x82"), "entry.png is truncated"
    assert len(data) <= 1_048_576, "entry.png exceeds the 1 MiB gate limit"
    output_path().write_bytes(data)


if __name__ == "__main__":
    main()
