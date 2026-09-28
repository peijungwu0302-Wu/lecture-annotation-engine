"""Collision-safe Phase 1 placement selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .geometry import BBox


@dataclass(frozen=True, slots=True)
class PlacementCandidate:
    region: str
    bbox: BBox
    score: float


@dataclass(frozen=True, slots=True)
class PlacementDecision:
    region: str
    bbox: BBox
    score: float
    halo_intrusion: bool


def select_placement(
    candidates: Iterable[PlacementCandidate],
    source_ink: Iterable[BBox],
    *,
    target_clearance: float = 0.01,
) -> PlacementDecision | None:
    """Choose the best candidate, allowing halo intrusion but never ink overlap."""

    inks = tuple(source_ink)
    safe_candidates = [
        candidate
        for candidate in candidates
        if not any(candidate.bbox.intersects(ink) for ink in inks)
    ]
    if not safe_candidates:
        return None

    clear = [
        candidate
        for candidate in safe_candidates
        if not any(
            candidate.bbox.intersects(ink.expanded(target_clearance)) for ink in inks
        )
    ]
    pool = clear or safe_candidates
    chosen = max(pool, key=lambda candidate: candidate.score)
    return PlacementDecision(
        region=chosen.region,
        bbox=chosen.bbox,
        score=chosen.score,
        halo_intrusion=not bool(clear),
    )
