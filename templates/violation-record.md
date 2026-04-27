# Violation record — template

**Standard version:** 1.0 (see `docs/standard.md`)

Use this when a limit was crossed, success was claimed without meeting criteria, or an executor attempted an action outside the contract. Purpose: **audit** and **policy improvement**, not blame theater.

---

## Record metadata

| Field | Value |
|-------|--------|
| `violation_id` | `VIO-________________` |
| `task_id` | |
| `execution_id` | |
| `detected_at` | ISO 8601 |
| `detected_by` | human id, automaton, or verifier name |
| `severity` | e.g. `attempted_unauthorized` / `overreach` / `false_completion` / `data_exposure_risk` |

## What was required

**Contract limit or rule (quote or reference):**  
- 

## What happened

**Observed behavior (facts, links to logs, diff ids, message ids):**  
- 

## Root cause (preliminary)

- 

## Containment

**Immediate action taken (revoke, block, revert):**  
- 

## Remediation

| Type | Action |
|------|--------|
| Technical | e.g. revert commit, fix permissions |
| Process | e.g. tighten default contract template for this class of task |
| Follow-up | New `task_id` if legitimate work still needed: |

## Disclosure (if applicable)

**Per org policy, report to:** `n/a` or team / tool / ticket id  
**Notes:** 

---

**Filed by:** `________` **Date:** `________`  
**Supervisor review (if required):** `________`
