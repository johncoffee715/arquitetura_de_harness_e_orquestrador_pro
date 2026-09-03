---
skill_name: hestia
task_id: AUT-W1-hestia
run_id: 10cfd1f2-c2d7-4583-b6da-855dfbedb173

selection_criteria:
  - Task requires helenization (R77: 3-layers)
  - Use global bindings by category (R75)
  - Catalog-first (R8)
  - Apply constrained decoding (R81)

ignition_steps:
  1. Validate input task against category bindings.
  2. Apply helenization R77 (3 layers: ontologia, firewall, mecânica).
  3. Execute with constrained decoding and frontmatter validation.
  4. Return helenized output with strict schema.

refutation_strategy:
  - Use firewall rules to reject invalid patterns.
  - Refute against category mismatches using category bindings.
  - Apply constrained decoding to prevent token overflow.
  - Enforce global frontmatter validation.