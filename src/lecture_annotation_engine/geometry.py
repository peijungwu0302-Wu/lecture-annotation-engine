"""Normalized page geometry used by the public skeleton APIs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BBox:
    """A rectangle in normalized page coordinates."""

    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.x < 0 or self.y < 0 or self.width <= 0 or self.height <= 0:
            raise ValueError("bbox values must be positive normalized coordinates")
        if self.x + self.width > 1 or self.y + self.height > 1:
            raise ValueError("bbox must remain within page bounds")

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def intersects(self, other: "BBox") -> bool:
        return not (
            self.right <= other.x
            or other.right <= self.x
            or self.bottom <= other.y
            or other.bottom <= self.y
        )

    def expanded(self, amount: float) -> "BBox":
        if amount < 0:
            raise ValueError("expansion amount cannot be negative")
        left = max(0.0, self.x - amount)
        top = max(0.0, self.y - amount)
        right = min(1.0, self.right + amount)
        bottom = min(1.0, self.bottom + amount)
        return BBox(left, top, right - left, bottom - top)
