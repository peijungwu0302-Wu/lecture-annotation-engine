from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


class PublicRepositoryContractTests(unittest.TestCase):
    def test_required_repository_structure_exists(self) -> None:
        required = [
            "README.md",
            "LICENSE",
            "SKILL.md",
            "AGENTS.md",
            "docs/architecture.md",
            "docs/specification-v1.md",
            "docs/course-profile.md",
            "docs/lecture-ir.md",
            "docs/placement-engine.md",
            "docs/enrichment.md",
            "docs/qa.md",
            "docs/prior-art.md",
            "schemas/course-profile.schema.json",
            "schemas/lecture-ir.schema.json",
            "templates/latex-overlay.tex",
        ]
        for relative in required:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

        for package in [
            "parser", "anchors", "translation", "math", "enrichment", "renderer"
        ]:
            self.assertTrue(
                (ROOT / "src" / "lecture_annotation_engine" / package / "__init__.py").is_file()
            )

    def test_readme_explains_scope_architecture_and_demo(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in [
            "Preserve the lecturer's visual language",
            "CourseProfile",
            "LectureIR",
            "Immutable source ink",
            "Phase 1",
            "synthetic-annotated.pdf",
            "Not production-ready",
        ]:
            self.assertIn(phrase, readme)
        self.assertIn("examples/preview/synthetic-annotated-page-1.png", readme)

    def test_agents_file_contains_non_negotiable_invariants(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
        for phrase in [
            "never rasterize a full source pdf",
            "preserve page count",
            "protect original source ink",
            "preserve source figures",
            "generated math must use math mode",
            "logical blocks",
            "at least two compilation passes",
            "visual-regression testing",
            "copyright-protected sample lecture content",
        ]:
            self.assertIn(phrase, agents)

    def test_skill_has_discoverable_frontmatter_and_complete_workflow(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", skill, flags=re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = yaml.safe_load(match.group(1))
        self.assertEqual("lecture-annotation-engine", frontmatter["name"])
        self.assertTrue(frontmatter["description"].startswith("Use when"))
        for phrase in [
            "Inspect before editing",
            "CourseProfile",
            "LectureIR",
            "immutable source ink",
            "logical blocks",
            "math normalization",
            "Free Space Map",
            "semantic lane",
            "enrichment budget",
            "Visual QA",
            "repair loop",
        ]:
            self.assertIn(phrase, skill)

    def test_prior_art_records_architecture_and_license_boundaries(self) -> None:
        prior_art = (ROOT / "docs/prior-art.md").read_text(encoding="utf-8")
        for url in [
            "https://github.com/PDFMathTranslate/PDFMathTranslate",
            "https://github.com/funstory-ai/BabelDOC",
            "https://github.com/GioGioBond/pdf-layout-translate",
            "https://github.com/ghbhiee/skills",
        ]:
            self.assertIn(url, prior_art)
        self.assertIn("AGPL-3.0", prior_art)
        self.assertIn("MIT", prior_art)
        self.assertIn("No source code was copied", prior_art)

    def test_only_synthetic_pdfs_are_public_fixtures(self) -> None:
        pdfs = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*.pdf"))
        self.assertEqual(
            [
                "examples/synthetic-input/synthetic-lecture.pdf",
                "examples/synthetic-output/synthetic-annotated.pdf",
            ],
            pdfs,
        )


if __name__ == "__main__":
    unittest.main()
