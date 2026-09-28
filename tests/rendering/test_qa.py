from __future__ import annotations

import unittest

from lecture_annotation_engine.qa import build_qa_report


class QaReportTests(unittest.TestCase):
    def test_report_flags_page_size_overlap_and_tiny_fonts(self) -> None:
        report = build_qa_report(
            source_page_count=1,
            output_page_count=1,
            source_page_sizes=[(595.276, 841.89)],
            output_page_sizes=[(595.276, 841.89)],
            generated_font_sizes=[7.5, 5.4, 6.0],
            actual_ink_overlap_count=1,
        )

        self.assertTrue(report.page_count_ok)
        self.assertTrue(report.page_sizes_ok)
        self.assertFalse(report.source_ink_overlap_ok)
        self.assertAlmostEqual(1 / 3, report.tiny_font_percentage)
        self.assertFalse(report.passed)

    def test_clean_report_passes(self) -> None:
        report = build_qa_report(
            source_page_count=2,
            output_page_count=2,
            source_page_sizes=[(595.276, 841.89)] * 2,
            output_page_sizes=[(595.276, 841.89)] * 2,
            generated_font_sizes=[7.0, 8.0],
            actual_ink_overlap_count=0,
        )
        self.assertTrue(report.passed)


if __name__ == "__main__":
    unittest.main()
