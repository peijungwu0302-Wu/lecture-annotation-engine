# Prior Art and License Notes

Phase 1 reviewed public project documentation for architectural ideas only. No source code was copied.

## Projects

### PDFMathTranslate / pdf2zh

[PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) demonstrates that scientific-PDF translation needs explicit formula, chart, contents, and annotation preservation. Its documentation also calls out paragraph regrouping, adaptive typesetting, cross-column/cross-page semantic consistency, and dynamic scaling.

**Lesson:** formula protection and semantic regrouping belong before translation; layout verification cannot be an afterthought.

**License:** AGPL-3.0. Incorporating or adapting its implementation could impose reciprocal obligations incompatible with this project's intended Apache-2.0 clean-room implementation. Ideas and public interfaces were studied; code was not reused.

### BabelDOC

[BabelDOC](https://github.com/funstory-ai/BabelDOC) presents document translation as an embeddable Python library with CLI/API surfaces and bilingual output rather than a one-off script.

**Lesson:** keep a reusable intermediate pipeline, translation adapters, and rendering boundaries so other programs can embed the engine.

**License:** AGPL-3.0. Treat implementation reuse as legally significant; this repository records independent contracts instead.

### pdf-layout-translate

[pdf-layout-translate](https://github.com/GioGioBond/pdf-layout-translate) separates scan detection, digital extraction, OCR, simple block merging, translation, rendering, and pipeline orchestration. It also highlights CJK font configuration as an output-integrity concern.

**Lesson:** route scanned and digital PDFs differently, keep geometry with text, and validate real CJK rendering. A direct overwrite-at-original-position strategy is insufficient for immutable source ink and inline bilingual reflow, so this project uses explicit occupancy and anchor models.

**License:** MIT. The permissive license allows reuse with notice, but Phase 1 still uses a clean-room implementation to keep provenance simple.

### Agent Skill translation wrappers

[ghbhiee/skills](https://github.com/ghbhiee/skills) documents a portable PDF-translation skill around BabelDOC, whole-document glossary extraction, bilingual output, and local configuration handling.

**Lesson:** agent workflows should keep credentials out of prompts and repositories, expose deterministic scripts, and make translation consistency a document-level concern.

**License:** no repository-wide license was visible in the reviewed project materials. Treat its code and prose as all-rights-reserved unless the maintainer clarifies terms; only high-level workflow lessons are recorded here.

## Resulting boundaries

This project adopts the concepts of semantic paragraph grouping, formula protection, geometry-aware translation, intermediate representation, adaptive placement, embedded CJK fonts, and visual regression. It adds immutable source-ink protection, profile-driven semantic lanes, enrichment budgeting, annotation islands, and an ordered repair loop as first-class contracts.
