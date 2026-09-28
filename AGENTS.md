# Engineering Invariants

These rules are non-negotiable for every change in this repository.

1. Never rasterize a full source PDF by default. Preserve vector text, equations, drawings, and native images where possible.
2. Preserve page count unless the user explicitly requests a different pagination policy.
3. Protect original source ink. Every visible original mark is immutable by default, including artifacts and existing annotations.
4. Preserve source figures and their native quality.
5. Generated math must use math mode and be normalized to proper LaTeX semantics.
6. Translation must attach to complete logical blocks, never arbitrary raw spans or individual source lines.
7. TikZ `remember picture` overlays require at least two compilation passes.
8. Placement changes require visual-regression testing in addition to geometry tests.
9. Copyright-protected sample lecture content must not enter public fixtures, screenshots, or generated outputs without verified permission.

## Working contract

- Inspect the rendered source before editing.
- Load or create a CourseProfile before inferring reusable layout policy.
- Build LectureIR before planning translation or annotations.
- Recompute free space after bilingual reflow and elastic-anchor adjustment.
- Treat actual source-ink overlap as approximately zero; the safety halo is soft.
- Start generated text at the 7-8 pt target. Never render it below 5.5 pt.
- Run the full test suite and inspect the latest rendered preview before committing placement or renderer changes.
