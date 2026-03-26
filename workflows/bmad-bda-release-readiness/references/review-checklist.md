# Release Readiness Checklist

Use this checklist before deciding `PASS`, `CONCERNS`, or `FAIL`.

## 1. Candidate Control

- Identify one branch and one commit as the review target.
- Confirm the target environment the review applies to.
- Confirm whether the rollout is `fresh-machine` or `existing-deployment`.
- Confirm there is no competing branch that could also be interpreted as the release candidate.

## 2. Evidence Quality

- Prefer fresh evidence from automated tests, coverage reports, and release-gate artifacts.
- If evidence is stale, say so explicitly.
- If evidence is missing, do not silently assume success.

## 3. Operational Safety

- Confirm current-state baseline exists for existing deployments, or record the evidence gap explicitly.
- Confirm deploy path exists.
- Confirm rollback path exists.
- Confirm observability and health checks exist.

## 4. Decision Integrity

- `PASS` requires no unresolved blockers.
- `CONCERNS` requires issues that are real but non-blocking.
- `FAIL` is required whenever branch ambiguity, missing rollback, missing existing-deployment baseline, or failing quality gates creates deployment risk.
