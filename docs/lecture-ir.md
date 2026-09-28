# LectureIR

LectureIR is a public, renderer-independent JSON format defined by [`schemas/lecture-ir.schema.json`](../schemas/lecture-ir.schema.json).

## Coordinate model

Bounding boxes use normalized page coordinates: `x`, `y`, `width`, and `height` are within `[0, 1]`; width and height are positive. Physical page dimensions remain in document metadata. Runtime geometry additionally rejects boxes whose right or bottom edge leaves the page.

## Records

- `document`: page size, orientation, page count, CourseProfile reference, and languages.
- `sourceRegions`: semantic type, text, page geometry, reading order, logical group, and immutable source-ink reference.
- `translations`: logical source-block attachment, target language, text, and math-normalized state.
- `annotations`: teaching-note type, semantic anchor, priority, preferred lane, font bounds, and layout constraints.

IDs make relationships explicit. Geometry or mask references may point to external binary occupancy artifacts; those masks are not embedded in JSON.

The schema cannot express every relational invariant. A production validator must additionally verify that references resolve, page numbers exist, `x + width <= 1`, `y + height <= 1`, and semantic anchors point to compatible nodes.
