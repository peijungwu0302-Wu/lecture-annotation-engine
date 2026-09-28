"""Semantic grouping primitives; translation attaches only after grouping."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class TextSpan:
    id: str
    page_number: int
    reading_order: int
    logical_group: str
    text: str


@dataclass(frozen=True, slots=True)
class LogicalBlock:
    id: str
    page_number: int
    text: str
    source_span_ids: tuple[str, ...]


def group_logical_blocks(spans: Iterable[TextSpan]) -> list[LogicalBlock]:
    """Group ordered raw spans into complete logical blocks."""

    ordered = sorted(spans, key=lambda span: (span.page_number, span.reading_order))
    groups: "OrderedDict[tuple[int, str], list[TextSpan]]" = OrderedDict()
    for span in ordered:
        groups.setdefault((span.page_number, span.logical_group), []).append(span)

    return [
        LogicalBlock(
            id=group_id,
            page_number=page_number,
            text=" ".join(span.text.strip() for span in members if span.text.strip()),
            source_span_ids=tuple(span.id for span in members),
        )
        for (page_number, group_id), members in groups.items()
    ]
