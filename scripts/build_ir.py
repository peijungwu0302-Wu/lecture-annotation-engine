"""Create a document-level LectureIR scaffold; semantic extraction is future work."""

from __future__ import annotations

import argparse
from pathlib import Path


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("pdf", nargs="?", type=Path)
    result.add_argument("--profile", type=Path)
    result.add_argument("--output", type=Path)
    return result


def main() -> int:
    parser().parse_args()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
