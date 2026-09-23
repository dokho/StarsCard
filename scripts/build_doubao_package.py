#!/usr/bin/env python3
"""Build the platform-neutral ZIP accepted by Volcengine skill importers."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


REQUIRED_FILES = (
    "SKILL.md",
    "references/production-workflow.md",
    "references/style-catalog.md",
    "references/style-system.md",
    "references/doubao-volcengine.md",
)


def build(repo_root: Path, output: Path) -> None:
    skill_root = repo_root / "stars-card-design"
    missing = [name for name in REQUIRED_FILES if not (skill_root / name).is_file()]
    if missing:
        raise SystemExit("Missing required skill files: " + ", ".join(missing))

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for relative_name in REQUIRED_FILES:
            archive.write(skill_root / relative_name, arcname=relative_name)

    print(f"Built {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dist/stars-card-design-doubao.zip"),
        help="Output ZIP path relative to the repository root.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    output = args.output if args.output.is_absolute() else repo_root / args.output
    build(repo_root, output)


if __name__ == "__main__":
    main()
