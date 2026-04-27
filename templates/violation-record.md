# Violation record — template

**Standard version:** 1.0 (see `docs/standard.md`)

Use this when a limit was crossed, success was claimed without meeting criteria, or an executor attempted an action outside the contract. **Normative:** if a violation is **detected**, the record **must** be **filed** and **linked** before task/review **closure** (see `docs/standard.md` §8). Purpose: **audit** and **policy improvement**, not blame theater.

---

## Enforcement fields (required for filing)

| Field | Value |
|-------|--------|
| `violation_id` | `VIO-________________` (stable id for this record) |
| `task_id` | Contract `task_id` this run belongs to |
| `execution_id` | Bound identity id when applicable; `n/a` only if violation is purely supervisor/control-plane with no executor |
| `detected_at` | ISO 8601 |
| `detected_by` | Human id, automaton, or verifier name |
| **Rule violated** | Quote or cite contract clause, policy id, or standard section (e.g. §1.1 bridge, `allowed_paths`) |
| **Evidence** | Facts only: diff ids, commit hashes, log excerpts, message ids, command transcripts (redact secrets) |
| **Containment** | Immediate action: revoke, block, revert, freeze branch—what was **done** |
| **Prevention** | Follow-up to reduce recurrence: template change, CI rule, checkpoint, training link |
| `status` | e.g. `filed` / `contained` / `remediated` / `closed` (per org workflow) |
| **Verification** | How this record and containment were **checked** (who/when, or “automated link from ticket #…”) |

## Optional: severity

| Field | Value |
|-------|--------|
| `severity` | e.g. `attempted_unauthorized` / `overreach` / `false_completion` / `data_exposure_risk` / `supervisor_overreach` |

## Root cause (preliminary)

- 

## Remediation detail (if not fully captured above)

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
