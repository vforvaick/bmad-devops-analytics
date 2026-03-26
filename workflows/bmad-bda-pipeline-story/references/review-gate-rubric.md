# Review Gate Rubric

Use this rubric when classifying automated review findings inside the story pipeline.

## Severity Levels

### Blocking

Classify as `blocking` when the story should not merge yet.

Examples:

- likely correctness bug in changed behavior
- missing guard on directly reachable boundary condition
- acceptance mismatch against the story or spec
- regression risk in critical path with no compensating test or guard
- review evidence is incomplete, unreadable, or contradictory

### Major

Classify as `major` when the issue is real and important, but can be merged only if the pipeline explicitly records the risk acceptance.

Examples:

- partial acceptance coverage with a documented and bounded gap
- important maintainability issue in newly changed critical code
- non-trivial operational risk with mitigations already in place

### Minor

Classify as `minor` when the issue is real but does not justify stopping the story pipeline.

Examples:

- follow-up refactor opportunity
- clarity or maintainability issue
- hardening improvement not directly reachable in the current change
- pre-existing issue surfaced by review but not introduced by the story diff

## Noise

Classify as `noise` when the item is not actionable for the current scope.

Examples:

- false positive contradicted by the diff
- duplicate with no added signal
- speculative concern unsupported by the provided scope

## Acceptance Audit Rules

- When a story or spec file exists, explicitly separate acceptance gaps from generic code-quality findings.
- Any unimplemented or contradicted must-have acceptance criterion is `blocking`.
- Any partially satisfied but non-critical acceptance criterion is at least `major`.

## Gate Decision Rules

- `FAIL` when any `blocking` finding exists.
- `PASS WITH RISKS` when there are no `blocking` findings but one or more `major` findings remain.
- `PASS` when only `minor` findings or `noise` remain.
