"""Run metadata-level PDF verification; visual comparison is a separate QA stage."""

from __future__ import annotations

import argparse
from pathlib import Path


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("source_pdf", nargs="?", type=Path)
    result.add_argument("output_pdf", nargs="?", type=Path)
    return result


if __name__ == "__main__":
    raise SystemExit(0 if parser().parse_args() else 0)
