from __future__ import annotations

import unittest

from lecture_annotation_engine.semantics import TextSpan, group_logical_blocks


class LogicalGroupingTests(unittest.TestCase):
    def test_spans_are_grouped_before_translation(self) -> None:
        spans = [
            TextSpan("s2", 1, 2, "p1", "logical block."),
            TextSpan("s1", 1, 1, "p1", "A complete"),
            TextSpan("s3", 1, 3, "p2", "Next paragraph."),
        ]

        blocks = group_logical_blocks(spans)

        self.assertEqual(["p1", "p2"], [block.id for block in blocks])
        self.assertEqual("A complete logical block.", blocks[0].text)
        self.assertEqual(("s1", "s2"), blocks[0].source_span_ids)


if __name__ == "__main__":
    unittest.main()
