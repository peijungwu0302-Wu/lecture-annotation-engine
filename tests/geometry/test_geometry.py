from __future__ import annotations

import unittest

from lecture_annotation_engine.geometry import BBox


class BoundingBoxTests(unittest.TestCase):
    def test_area_and_intersection_use_normalized_page_space(self) -> None:
        first = BBox(0.10, 0.10, 0.30, 0.20)
        second = BBox(0.35, 0.20, 0.20, 0.20)
        distant = BBox(0.70, 0.70, 0.10, 0.10)

        self.assertAlmostEqual(0.06, first.area)
        self.assertTrue(first.intersects(second))
        self.assertFalse(first.intersects(distant))

    def test_box_crossing_page_boundary_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "page bounds"):
            BBox(0.90, 0.20, 0.20, 0.10)


if __name__ == "__main__":
    unittest.main()
