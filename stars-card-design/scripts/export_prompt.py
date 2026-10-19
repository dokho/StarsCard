#!/usr/bin/env python3
"""Export the canonical skill as one standalone, tool-neutral chat instruction."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

DOCUMENTS = (
    "SKILL.md", "references/capabilities.md", "references/preferences.md",
    "references/input-spec.md", "references/photo-fidelity.md", "references/design-styles.md",
    "references/style-catalog.md", "references/style-system.md", "references/production-workflow.md",
    "references/print-production.md", "references/doubao-volcengine.md",
    "references/delivery-qa.md", "references/tooling.md", "references/platforms.md",
)
TEMPLATES = ("assets/intake.template.json", "assets/print-job.template.json")


def inline_local_links(text: str) -> str:
    # Relative file links are inaccessible to a chat receiving only this document.
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: m.group(0) if m.group(2).startswith(("https://", "http://", "#"))
                  else f"{m.group(1)}（见本文件对应章节）", text)


def render(skill_root: Path) -> str:
    intro = """# 球星卡制作 · 通用制卡指令

版本：1.1.0；技能标识：stars-card-design。

把本文件作为当前制卡任务的工作说明，结合用户接下来给出的照片和要求执行。用户的新选择和宿主规则优先。本文件本身不要求安装某个平台、连接账号、付费 API 或提供密钥。

这是完整的单文件指令，已合并主入口、参考正文和输入模板。文中“读取某文件”表示查找下方同名章节，不代表你已经能访问该文件夹。未提供真实素材时，不以模板内容当作球员资料。只粘贴本文件不会把 Python 脚本部署到运行环境。

先使用你实际具备的看图、参考图编辑、原图排版与文件能力；能做图就完成实际图像，只有文本能力就给设计/编辑提示词和人工制作步骤，不编造已生成的图片、PDF 或链接。需要脚本时，用户需另提供完整技能文件夹；没有读到或运行脚本就标为未执行。

本文件会较长；若宿主上下文容量有限，用户可只粘贴核心规则、能力适配和当前任务所需章节。不要以未收到的章节作为已读依据。

---

"""
    chunks = [intro]
    for relative in DOCUMENTS:
        content = (skill_root / relative).read_text(encoding="utf-8-sig")
        if relative == "SKILL.md":
            content = re.sub(r"\A---\r?\n.*?\r?\n---\r?\n", "", content, count=1, flags=re.S)
        chunks.append(f"## 原文件：{relative}\n\n{inline_local_links(content).strip()}\n\n---\n\n")
    for relative in TEMPLATES:
        chunks.append(f"## 输入模板：{relative}\n\n```json\n" +
                      (skill_root / relative).read_text(encoding="utf-8").strip() + "\n```\n\n")
    return "".join(chunks).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    skill_root = Path(__file__).resolve().parent.parent
    output = args.output or skill_root / "通用制卡指令.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(skill_root), encoding="utf-8")
    print(f"Exported {output}")


if __name__ == "__main__":
    main()
