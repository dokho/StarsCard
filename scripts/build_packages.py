#!/usr/bin/env python3
"""Build folder-root Agent Skills ZIP and root-SKILL legacy importer ZIP."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def build(repo_root: Path, output_dir: Path) -> list[Path]:
    skill_root = repo_root / "stars-card-design"
    spec = importlib.util.spec_from_file_location("portable_export", skill_root / "scripts" / "export_prompt.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    (skill_root / "通用制卡指令.md").write_text(module.render(skill_root), encoding="utf-8")
    files = sorted(p for p in skill_root.rglob("*") if p.is_file()
                   and "__pycache__" not in p.parts and p.suffix != ".pyc")
    if not (skill_root / "SKILL.md").is_file():
        raise ValueError("Missing SKILL.md")
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for filename, folder_root in (("stars-card-design-portable.zip", True),
                                  ("stars-card-design-doubao.zip", False)):
        output = output_dir / filename
        with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for path in files:
                relative = path.relative_to(skill_root)
                if not folder_root and relative.parts[0] == "agents":
                    continue
                name = (Path("stars-card-design") / relative if folder_root else relative).as_posix()
                # Stable metadata makes the same source bytes produce the same ZIP.
                from zipfile import ZipInfo
                info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                data = path.read_bytes()
                if path.suffix in (".md", ".py", ".json", ".yaml", ".yml", ".txt"):
                    data = data.replace(b"\r\n", b"\n")
                archive.writestr(info, data)
        outputs.append(output)
    sums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in outputs)
    (output_dir / "SHA256SUMS.txt").write_text(sums, encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    for output in build(repo_root, args.output_dir or repo_root / "dist"):
        print(f"Built {output}")


if __name__ == "__main__":
    main()
