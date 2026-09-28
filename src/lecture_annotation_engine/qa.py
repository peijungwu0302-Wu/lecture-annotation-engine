"""Machine-readable Phase 1 visual-QA summaries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class QaReport:
    page_count_ok: bool
    page_sizes_ok: bool
    source_ink_overlap_ok: bool
    tiny_font_percentage: float

    @property
    def passed(self) -> bool:
        return (
            self.page_count_ok
            and self.page_sizes_ok
            and self.source_ink_overlap_ok
            and self.tiny_font_percentage == 0
        )


def build_qa_report(
    *,
    source_page_count: int,
    output_page_count: int,
    source_page_sizes: Sequence[tuple[float, float]],
    output_page_sizes: Sequence[tuple[float, float]],
    generated_font_sizes: Iterable[float],
    actual_ink_overlap_count: int,
) -> QaReport:
    fonts = tuple(generated_font_sizes)
    tiny = sum(size < 5.5 for size in fonts)
    page_sizes_ok = (
        len(source_page_sizes) == source_page_count
        and len(output_page_sizes) == output_page_count
        and all(
            abs(source[0] - output[0]) < 0.01
            and abs(source[1] - output[1]) < 0.01
            for source, output in zip(source_page_sizes, output_page_sizes)
        )
    )
    return QaReport(
        page_count_ok=source_page_count == output_page_count,
        page_sizes_ok=page_sizes_ok,
        source_ink_overlap_ok=actual_ink_overlap_count == 0,
        tiny_font_percentage=tiny / len(fonts) if fonts else 0.0,
    )
