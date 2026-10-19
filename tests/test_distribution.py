import hashlib
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "stars-card-design"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DistributionTests(unittest.TestCase):
    def test_all_relative_markdown_references_exist(self):
        files = [ROOT / "README.md", *(SKILL.rglob("*.md"))]
        for doc in files:
            for target in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8-sig")):
                if target.startswith(("https://", "http://", "#")):
                    continue
                with self.subTest(doc=doc.name, target=target):
                    self.assertTrue((doc.parent / target.split("#")[0]).exists())

    def test_single_file_is_complete_and_not_drifting(self):
        exporter = load("exporter", SKILL / "scripts" / "export_prompt.py")
        rendered = exporter.render(SKILL)
        self.assertEqual((SKILL / "通用制卡指令.md").read_text(encoding="utf-8"), rendered)
        self.assertNotRegex(rendered, r"\]\((?!https?://|#)[^)]+\)")
        for document in (*exporter.DOCUMENTS, *exporter.TEMPLATES):
            self.assertIn(document, rendered)
        self.assertFalse(rendered.startswith("---"))

    def test_two_archive_layouts_and_deterministic_bytes(self):
        builder = load("builder", ROOT / "scripts" / "build_packages.py")
        with tempfile.TemporaryDirectory() as tmp:
            paths = builder.build(ROOT, Path(tmp))
            before = {p.name: p.read_bytes() for p in paths}
            for path in paths:
                with ZipFile(path) as z:
                    self.assertIsNone(z.testzip())
                    names = z.namelist()
                    prefix = "stars-card-design/" if "portable" in path.name else ""
                    self.assertIn(prefix + "SKILL.md", names)
                    self.assertIn(prefix + "scripts/impose_cards.py", names)
                    self.assertIn(prefix + "references/capabilities.md", names)
                    self.assertIn(prefix + "references/style-catalog.md", names)
                    self.assertIn(prefix + "通用制卡指令.md", names)
                    self.assertTrue(all(n.startswith(prefix) for n in names))
                    self.assertFalse(any(".." in Path(n).parts or "__pycache__" in n for n in names))
                    if not prefix:
                        self.assertFalse(any(n.startswith("agents/") for n in names))
                    for n in names:
                        relative = n[len(prefix):]
                        expected = (SKILL / relative).read_bytes()
                        if Path(relative).suffix in (".md", ".py", ".json", ".yaml", ".yml", ".txt"):
                            expected = expected.replace(b"\r\n", b"\n")
                        self.assertEqual(z.read(n), expected)
            for line in (Path(tmp) / "SHA256SUMS.txt").read_text().splitlines():
                digest, name = line.split("  ", 1)
                self.assertEqual(hashlib.sha256((Path(tmp) / name).read_bytes()).hexdigest(), digest)
            rebuilt = builder.build(ROOT, Path(tmp))
            self.assertEqual(before, {p.name: p.read_bytes() for p in rebuilt})

    def test_all_json_templates_parse(self):
        for path in (SKILL / "assets").glob("*.json"):
            with self.subTest(path=path.name):
                self.assertIsInstance(json.loads(path.read_text(encoding="utf-8")), dict)

    def test_skill_metadata_is_portable(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: stars-card-design\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertNotIn("allowed-tools:", frontmatter)
        self.assertNotIn("context:", frontmatter)
        self.assertNotIn("model:", frontmatter)
        self.assertLessEqual(len(re.search(r"^description: (.+)$", frontmatter, re.M)[1]), 200)


if __name__ == "__main__":
    unittest.main()
