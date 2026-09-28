# Architecture

Lecture Annotation Engine is a pipeline of public contracts and replaceable components rather than a monolithic PDF editor.

```text
PDF -> Parser -> Semantic Grouping -> LectureIR -> Anchor Graph
                                              -> Bilingual Reflow
                                              -> Region/Lane Planner
Enrichment Candidates ----------------------> Planner
Planner -> Renderer -> Visual QA -> Repair -> Renderer
```

## Boundaries

- **Parser** recovers spans, geometry, figures, equations, and page furniture without mutating the source.
- **Semantic grouping** turns spans into headings, paragraphs, definitions, results, proofs, exercises, figures, captions, and source artifacts.
- **CourseProfile** supplies course-level layout policies; page observations do not silently become global rules.
- **LectureIR** is the renderer-independent exchange format.
- **Anchor graph** encodes fixed, elastic-frame, structural, and flow relationships.
- **Bilingual reflow** attaches translations after complete logical English blocks.
- **Planner** scores natural whitespace, profile lanes, annotation islands, eligible anchor movement, and footer reserve while protecting source ink.
- **Enrichment engine** generates more candidates than the page must display; priority and capacity decide visibility.
- **Renderer** composes vector overlays and Unicode-safe CJK text without full-page rasterization.
- **Visual QA / repair** closes the loop with geometry, content, and rendered-image checks.

Phase 1 implements contracts and small deterministic primitives. Production extraction, translation, optimization, and rendering remain later phases.
