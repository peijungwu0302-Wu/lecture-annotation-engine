# Lecture Annotation Engine Specification v1.0

Status: Phase 1 public contract

## Mission

Lecture Annotation Engine augments lecture PDFs without redesigning them. It preserves the lecturer's visual language and adds inline bilingual translation, LaTeX-normalized mathematics, pedagogical explanation, derivation and proof notes, exercise solutions, figure-reading guidance, revision cues, tips, and common-mistake warnings.

The architecture is:

`CourseProfile -> LectureIR -> Anchor Graph -> Bilingual Reflow -> Region/Lane Planner -> Enrichment Engine -> Renderer -> Visual QA / Repair Loop`

The components are separable public interfaces. A monolithic PDF-editing script is out of scope.

## CourseProfile

A CourseProfile captures recurring course-level properties rather than page-specific observations:

- page size and orientation;
- source typography, margins, visual identity, and figure-preservation policy;
- candidate left and right lanes with reliability, confidence, and semantic roles;
- supported anchor classes;
- translation and annotation target font of 7-8 pt and minimum font of 5.5 pt;
- inline translation placement after a complete logical English block;
- mandatory generated-math normalization;
- an elastic, configurable footer reserve;
- enrichment coverage of 100%, unbounded candidate-generation depth, constrained visible density, and a default whitespace-fill cap of 0.60-0.70;
- collision policy with approximately zero source-ink overlap, a soft safety halo, about 3 mm target clearance, and 1-1.5 mm preferred minimum clearance.

Lane roles are profile-driven. No margin is globally assumed usable. The example profile may identify reliable left revision and right explanation lanes.

## LectureIR

LectureIR is renderer-independent JSON with a public JSON Schema. It records:

- document page geometry, orientation, course-profile reference, and languages;
- source regions including headings, paragraphs, definitions, examples, theorems, results, proofs, exercises, figures, equations, captions, headers, footers, page numbers, and source artifacts;
- page-numbered bounding boxes, preferred positions, anchor classes, reading order, and logical groups;
- immutable source-ink flags and geometry or mask references;
- translations attached to logical source blocks, target language, and math-normalized state;
- annotations with semantic anchor, type, priority, preferred lane, and font bounds;
- layout constraints for preferred region, collision tolerance, minimum clearance, and movement allowance.

## Immutable Source Ink

Every visible mark in the original render is protected by default, including glyphs, equations, figures, vectors, rules, page furniture, page numbers, black squares, scanning artifacts, and existing annotations. The engine must not infer that a source mark is a mistake. Removal requires an explicit user request.

## Logical Grouping and Translation

Translation operates on semantic blocks:

`raw spans -> semantic grouping -> logical English block -> Chinese translation`

A complete paragraph remains intact. English and Chinese form one bilingual unit, with Chinese immediately after its English block. Side-by-side columns require an explicit CourseProfile policy.

## Math Normalization

Generated mathematical semantics inside Chinese text use LaTeX math mode. Normalization includes forms such as `\mathbb{R}^3`, `x_1=x_2`, `\operatorname{Proj}_u(v)`, and `\lVert u\rVert^2`. Source notation is preserved where possible. Math normalization is a QA requirement.

## Anchors and Reflow

The anchor graph supports:

- `fixed`: page geometry, major header identity, and major figures where possible;
- `elastic-frame`: footer rule, footer text, and page-number region, movable toward the page boundary;
- `structural`: definitions, examples, results, proofs, and displayed equations, with order and x-alignment preserved and moderate vertical movement allowed;
- `flow`: ordinary paragraphs and inline translations with flexible vertical reflow.

Horizontal source geometry is normally stronger than vertical geometry.

## Free Space and Placement

The planner computes free space only after source parsing, logical grouping, bilingual insertion, anchor reflow, and elastic footer adjustment. It then recomputes occupancy from source ink, translations, already placed notes, and safety halos, using PDF geometry and rendered occupancy when useful.

Actual source ink is a hard protected area. The safety halo is soft and may be slightly intruded in emergencies. Placement order is:

1. nearby natural whitespace;
2. semantic margin lane;
3. annotation island;
4. soft structural-anchor movement;
5. elastic footer reserve;
6. gradual font reduction;
7. optional-content removal;
8. distributed proof as a last resort.

Placement scoring penalizes whitespace fragmentation. Notes for one concept should form a coherent annotation island when possible.

## Enrichment

Every important Definition, Example, Result, Theorem, Proof, Exercise, and Figure is evaluated (`coverage = 100%`). Candidate-generation depth is unbounded. Visible density remains constrained by capacity, collision safety, and layout quality.

Required enrichment includes definition intuition, example explanation, important omitted proof steps, and pedagogically useful exercise solutions. High-priority enrichment includes result meaning, derivations, and figure-reading guides. Tips, memory cues, common mistakes, and future-topic connections are optional and may be dropped from visible output.

## Rendering

Output remains a standard, lightweight, iPad-friendly PDF. Source vectors and images stay vector or native where possible; full-page rasterization is not the default. Generated math remains vector LaTeX, and CJK rendering is Unicode-safe. TikZ `remember picture` overlays require at least two LaTeX passes. Page count remains unchanged unless explicitly requested.

## Visual QA and Repair

QA covers page count and size, source-figure integrity, source-ink preservation, Chinese glyph validity, math normalization, translation association, actual overlap, safety clearance, fragmentation, tiny-font percentage, footer displacement, layout similarity, and rendered visual regression.

Repair order is: move within region, switch lane, shift structural/flow anchors, use footer reserve, shrink gradually, drop optional enrichment, then distribute as a final fallback. Every repair is re-rendered and re-checked.

## Copyright Safety

Copyright-protected lecture PDFs and their complete translated or annotated derivatives are not public fixtures without verified redistribution permission. Phase 1 uses only an intentionally synthetic lecture containing a Definition, Example, Result, Proof, Exercise, Figure, equations, left and right margins, a footer, and an artificial source artifact.

## Phase 1 Boundary

Phase 1 delivers documentation, CourseProfile and LectureIR schemas, a portable workflow skill, engineering invariants, a synthetic input/output pair, small parser/layout/QA skeletons, and tests. It does not provide OCR, live translation, production-grade semantic extraction, a complete optimization solver, or arbitrary-PDF rendering.
