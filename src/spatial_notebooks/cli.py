"""`summarize` CLI — Phase 1 milestone practice."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from spatial_notebooks.stats import load_csv, summarize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print summary stats for a CSV file.")
    parser.add_argument("path", help="Path to a CSV file")
    args = parser.parse_args(argv)

    df = load_csv(args.path)
    summary = summarize(df)
    print(json.dumps(asdict(summary), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
