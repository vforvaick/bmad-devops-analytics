# Deployment Plan: [Release Version / Name]

**Date**: [YYYY-MM-DD]
**Candidate**: [branch @ commit]
**Target Environment**: [environment]
**Deployment Mode**: [fresh-machine | existing-deployment]
**Operator**: [name or agent]
**Execution Mode**: [live | dry-run | planning-only]

## Summary
[Short description of what will be deployed and why this path is safe.]

## Preconditions
- [ ] `release-readiness.md` decision is PASS for the same candidate
- [ ] Target environment identity is confirmed
- [ ] Baseline or greenfield prerequisites are recorded
- [ ] Observability contract is available
- [ ] Rollback target is known

## Deployment Sequence
1. **Prepare**
   - [exact step]
2. **Protect Current State**
   - [exact step]
3. **Run Migrations**
   - [exact step or N/A]
4. **Deploy Application**
   - [exact step]
5. **Run Smoke Tests**
   - [exact step]
6. **Observe Immediate Signals**
   - [exact step]

## Migration Strategy
- **Required**: [yes | no]
- **Mode**: [forward-only | reversible]
- **Risk Notes**: [notes]

## Smoke Test Plan
- **System Health Path**: [test]
- **Critical User Journey**: [test]
- **Release Marker Verification**: [test]
- **Observability Check**: [test]

## Rollback Triggers
1. [trigger]
2. [trigger]

## Rollback Procedure
1. [exact rollback step]
2. [exact verification step]

## Evidence References
- **Release Readiness**: [path]
- **Deployment Baseline**: [path or N/A]
- **Observability Config**: [path]
