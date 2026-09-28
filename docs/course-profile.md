# CourseProfile

CourseProfile describes recurring behavior of a course or lecturer, not one page. The public schema is [`schemas/course-profile.schema.json`](../schemas/course-profile.schema.json); [`profiles/example-course.yaml`](../profiles/example-course.yaml) is synthetic.

## Main groups

| Group | Purpose |
|---|---|
| `page` | Canonical point dimensions and orientation. |
| `sourceStyle` | Typography, body font, margins, visual identity, figure policy. |
| `lanes` | Side, availability, reliability, confidence, semantic role. |
| `anchors` | Required fixed, elastic-frame, structural, and flow classes. |
| `translation`, `annotation` | Target 7-8 pt and minimum 5.5 pt. |
| `footer` | Elastic downward reserve. |
| `enrichment` | 100% coverage, unbounded generation, constrained visible density. |
| `collision` | Approximately zero ink overlap and soft clearance halo. |

The planner must measure lane reliability across a representative page sample. The synthetic profile records a reliable left revision lane and right explanation lane; other courses may expose one lane or none.
