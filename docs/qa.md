# Visual QA and Repair

QA combines structural, semantic, geometric, and rendered checks.

## Checks

- page count and physical page size;
- source figure and source-ink preservation;
- valid CJK glyphs and embedded fonts;
- math normalization and vector math output;
- translation-to-logical-block association;
- actual ink overlap and soft-halo clearance;
- annotation-island fragmentation;
- percentage of generated text below 5.5 pt;
- footer displacement and anchor movement;
- layout similarity and pixel/vector visual regression.

## Repair order

1. move the note within its current region;
2. switch to another reliable semantic lane;
3. shift eligible structural or flow anchors;
4. use elastic footer reserve;
5. shrink gradually, never below 5.5 pt;
6. drop optional enrichment;
7. distribute a logical annotation only as the final fallback.

Every repair produces a fresh render and repeats the relevant checks. A successful metadata check is not a substitute for inspecting the rendered page.
