#!/usr/bin/env python3
"""Backward-compatible wrapper for the existing root-SKILL importer package."""
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path
from build_packages import build as build_packages


def build(repo_root: Path, output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="stars-card-package-") as temporary:
        packages = build_packages(repo_root, Path(temporary))
        data = next(p for p in packages if p.name == "stars-card-design-doubao.zip").read_bytes()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
    print(f"Built {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist/stars-card-design-doubao.zip"))
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    build(repo_root, args.output if args.output.is_absolute() else repo_root / args.output)


if __name__ == "__main__":
    main()
