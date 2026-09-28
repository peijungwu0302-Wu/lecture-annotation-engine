"""Public Phase 1 primitives for the Lecture Annotation Engine."""

from .geometry import BBox
from .layout import PlacementCandidate, PlacementDecision, select_placement
from .qa import QaReport, build_qa_report
from .semantics import LogicalBlock, TextSpan, group_logical_blocks

__all__ = [
    "BBox",
    "LogicalBlock",
    "PlacementCandidate",
    "PlacementDecision",
    "QaReport",
    "TextSpan",
    "build_qa_report",
    "group_logical_blocks",
    "select_placement",
]
