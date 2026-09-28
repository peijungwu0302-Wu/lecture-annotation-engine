from __future__ import annotations

import unittest
from pathlib import Path

from pypdf import PdfReader
from scripts.generate_synthetic_demo import ARTIFACT_BOX_PT, RIGHT_LANE_BOX_PT


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "examples/synthetic-input/synthetic-lecture.pdf"
OUTPUT = ROOT / "examples/synthetic-output/synthetic-annotated.pdf"
PREVIEW = ROOT / "examples/preview/synthetic-annotated-page-1.png"


class SyntheticDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = PdfReader(SOURCE)
        cls.output = PdfReader(OUTPUT)

    def test_page_count_and_a4_geometry_are_preserved(self) -> None:
        self.assertEqual(1, len(self.source.pages))
        self.assertEqual(len(self.source.pages), len(self.output.pages))
        for source_page, output_page in zip(self.source.pages, self.output.pages):
            source_size = (float(source_page.mediabox.width), float(source_page.mediabox.height))
            output_size = (float(output_page.mediabox.width), float(output_page.mediabox.height))
            self.assertAlmostEqual(595.276, source_size[0], places=2)
            self.assertAlmostEqual(841.89, source_size[1], places=2)
            self.assertEqual(source_size, output_size)

    def test_source_contains_all_synthetic_knowledge_nodes(self) -> None:
        text = self.source.pages[0].extract_text()
        for label in ["Definition", "Example", "Result", "Proof", "Exercise", "Figure"]:
            self.assertIn(label, text)
        self.assertIn("SOURCE ARTIFACT", text)

    def test_annotated_output_preserves_artifact_and_adds_teaching_layers(self) -> None:
        text = self.output.pages[0].extract_text()
        self.assertIn("SOURCE ARTIFACT", text)
        self.assertIn("中譯", text)
        for label in ["Revision cue", "Intuition", "Derivation", "Figure guide", "Common mistake"]:
            self.assertIn(label, text)

    def test_demo_does_not_contain_reference_identifiers(self) -> None:
        text = "\n".join(
            [self.source.pages[0].extract_text(), self.output.pages[0].extract_text()]
        ).lower()
        forbidden = [
            "linear_algebra_p1_12_bilingual_notes_v4_4",
            "prof. chingnun lee",
            "nsysu",
            "tongji university",
        ]
        for value in forbidden:
            self.assertNotIn(value, text)

    def test_generated_cjk_font_is_embedded(self) -> None:
        fonts = self.output.pages[0]["/Resources"]["/Font"]
        embedded = False
        for reference in fonts.values():
            font = reference.get_object()
            descriptor = font.get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                embedded |= any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
            for descendant in font.get("/DescendantFonts", []):
                descriptor = descendant.get_object().get("/FontDescriptor")
                if descriptor:
                    descriptor = descriptor.get_object()
                    embedded |= any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
        self.assertTrue(embedded, "generated CJK text must use an embedded font")

    def test_preview_exists_and_is_nonempty(self) -> None:
        self.assertGreater(PREVIEW.stat().st_size, 10_000)

    def test_right_lane_does_not_cross_the_source_artifact(self) -> None:
        ax, ay, aw, ah = ARTIFACT_BOX_PT
        rx, ry, rw, rh = RIGHT_LANE_BOX_PT
        intersects = not (
            ax + aw <= rx or rx + rw <= ax or ay + ah <= ry or ry + rh <= ay
        )
        self.assertFalse(intersects)


if __name__ == "__main__":
    unittest.main()
