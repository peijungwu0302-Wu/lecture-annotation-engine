from __future__ import annotations

import unittest

from lecture_annotation_engine.geometry import BBox
from lecture_annotation_engine.layout import PlacementCandidate, select_placement


class PlacementTests(unittest.TestCase):
    def test_actual_source_ink_overlap_is_never_selected(self) -> None:
        ink = [BBox(0.20, 0.20, 0.40, 0.20)]
        candidates = [
            PlacementCandidate("nearby", BBox(0.25, 0.25, 0.10, 0.08), 100),
            PlacementCandidate("right-lane", BBox(0.70, 0.20, 0.18, 0.12), 80),
        ]

        chosen = select_placement(candidates, ink)

        self.assertIsNotNone(chosen)
        self.assertEqual("right-lane", chosen.region)
        self.assertFalse(chosen.halo_intrusion)

    def test_soft_halo_intrusion_is_used_only_after_clear_candidates(self) -> None:
        ink = [BBox(0.20, 0.20, 0.20, 0.20)]
        close = PlacementCandidate("left-lane", BBox(0.405, 0.20, 0.10, 0.10), 90)

        chosen = select_placement([close], ink, target_clearance=0.02)

        self.assertIsNotNone(chosen)
        self.assertTrue(chosen.halo_intrusion)

    def test_no_candidate_returns_none_instead_of_overlapping_ink(self) -> None:
        ink = [BBox(0.20, 0.20, 0.40, 0.40)]
        blocked = PlacementCandidate("island", BBox(0.30, 0.30, 0.10, 0.10), 100)
        self.assertIsNone(select_placement([blocked], ink))


if __name__ == "__main__":
    unittest.main()
