"""Inspect PDF page geometry without mutating the source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("pdf", nargs="?", type=Path, help="PDF to inspect")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.pdf is None:
        return 0
    from pypdf import PdfReader

    reader = PdfReader(args.pdf)
    pages = [
        {"page": number, "widthPt": float(page.mediabox.width), "heightPt": float(page.mediabox.height)}
        for number, page in enumerate(reader.pages, start=1)
    ]
    print(json.dumps({"pageCount": len(pages), "pages": pages}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
