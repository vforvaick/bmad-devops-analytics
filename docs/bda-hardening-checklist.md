# BDA Hardening Checklist

This checklist defines the intended production-grade contract for BMAD DevOps Analytics (BDA).

## Lifecycle Alignment

- [x] BDA starts after BMAD sprint planning has produced a usable sprint/epic backlog.
- [x] Epic and story delivery workflows are the implementation entry point for BDA.
- [x] Production workflows start only after implementation pipelines have produced a real release candidate.
- [x] Observability is treated as a deployment prerequisite or an explicit exception, not an afterthought.

## Implementation Automation

- [x] Story delivery runs inside isolated git worktrees.
- [x] Epic delivery runs stories sequentially, never with overlapping write ownership.
- [x] Story merge is blocked on review or traceability failures.
- [x] Existing temporary story branches/worktrees are treated as recovery states, not silently overwritten.
- [x] Canonical branch drift before merge requires re-sync and re-verification.

## Deployment Safety

- [x] Release readiness evaluates one concrete candidate branch and commit at a time.
- [x] Release readiness and deployment both classify the target as either `fresh-machine` or `existing-deployment`.
- [x] Existing deployments require a current-state baseline snapshot before mutation unless the user explicitly overrides.
- [x] Existing VPS deployments are assessed from repo docs and prior production artifacts first; live host inspection is targeted fallback, not default behavior.
- [x] Rollback and database restore posture are reviewed before production changes.
- [x] Deployment records baseline, candidate, operator, timestamps, smoke results, and rollback outcomes.

## Observability And Evidence

- [x] Observability setup supports fully automated mode where an adapter exists.
- [x] Placeholder adapters must degrade to planning/manual-evidence mode instead of pretending automation exists.
- [x] Observability defines a telemetry contract for critical services and critical user journeys, not just infrastructure dashboards.
- [x] Observability defines release markers or version tagging so production evidence can be tied to one deploy candidate.
- [x] Observability defines alert ownership, notification path, and concise runbook guidance for high-risk failures.
- [x] Observability includes retention, privacy, and cost controls for the evidence path.
- [x] Existing deployments assess current observability coverage and gap-closure needs before rollout.
- [x] Existing observability stacks are reused, extended, corrected, or replaced based on documented evidence rather than greenfield assumptions.
- [x] Post-launch review states the evidence window, reviewed candidate, and confidence gaps explicitly.
- [x] Post-launch review compares production evidence against pre-deploy expectations and current baseline.
- [x] Post-launch review treats missing telemetry on critical paths as a real finding, not a minor note.

## BMAD Feedback Loop

- [x] Post-launch review produces durable production artifacts, not just conversational output.
- [x] BDA extracts release ground truth from BMAD foundation artifacts into a stable release-intent matrix.
- [x] BDA compares production evidence against that release-intent matrix, not only against narrative summaries.
- [x] Spec refinement keeps draft PRD and epic outputs separate from official planning documents.
- [x] Spec refinement can route evidence into `/bmad-correct-course` when current sprint or active epic changes are needed.
- [x] Future-sprint work remains suitable for standard BMAD sprint planning.

## Naming And Integration

- [x] Canonical workflow names use the `bmad-bda-*` prefix consistently.
- [x] Module metadata and agent metadata refer to the same canonical workflow names.
- [x] Docs describe the same happy path enforced by workflow preconditions.
- [x] Production artifacts use canonical templates with stable headings and `N/A` for intentionally empty fields.
- [x] Production artifacts can be validated by script, not only by human review.
- [x] Current-state artifacts are separated from run-history artifacts so repeated releases do not overwrite evidence.
- [x] PRD change proposals use release-linked draft names instead of open-ended `v2`, `v3`, `v4` naming.
- [x] Spec refinement names the exact BMAD original follow-up route and expected downstream artifact, including `sprint-change-proposal-{date}.md` for `/bmad-correct-course`.
- [x] Spec refinement emits a reusable BMAD follow-up package instead of leaving the next workflow as conversation-only guidance.
