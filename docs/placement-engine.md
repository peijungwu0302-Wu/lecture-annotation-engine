# Placement Engine

Placement begins only after source parsing, semantic grouping, bilingual insertion, anchor reflow, and elastic-footer adjustment.

```text
FreeSpace = PageArea - SourceInk - Translation - PlacedNotes - SafetyHalo
```

PDF bounding boxes provide precise geometry; rendered occupancy catches vector fills, artifacts, and marks missed by text extraction. Actual source ink is protected. The safety halo targets about 3 mm clearance, prefers at least 1-1.5 mm, and may be intruded only when the candidate still avoids ink.

## Candidate order

1. nearby natural whitespace;
2. reliable semantic margin lane;
3. coherent annotation island;
4. moderate structural/flow movement;
5. elastic footer reserve;
6. gradual font reduction;
7. removal of optional enrichment;
8. distributed proof as final fallback.

Scoring includes semantic distance, lane suitability, clearance, movement cost, and whitespace-fragmentation penalty. Notes attached to one concept should remain one island whenever capacity allows.

Phase 1's `select_placement` primitive demonstrates hard source-ink rejection and soft-halo fallback; it is not the full optimizer.
