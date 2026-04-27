# Contract fields — field-by-field guidance

Use these names (or a documented mapping to your org’s schema). Empty `allowed_paths` with no explicit non-file API allowance means **no** filesystem mutation.

## Identifiers and versioning

| Field | Guidance |
|-------|----------|
| `task_id` | Stable across retries; new scope ⇒ new id (or documented `supersedes` chain). |
| `version` | Contract schema version (e.g. `1.0`), not your app version. |
| `summary` | One line: **outcome**, not implementation steps. |
| `supervisor` | Accountable approver (user, role, team id). Required for delegated or risky work. |
| `supersedes` | Optional; prior `task_id` this contract replaces—keeps audit chain. |

## Intent

| Field | Guidance |
|-------|----------|
| `intent` | Plain-language **goal** and what “good” means for the org. |
| Non-goals | Explicit **anti-scope**: refactors, deps, envs, or features that must **not** be touched. |

Ambiguous intent ⇒ **Type D**; resolve before mutation.

## Time

| Field | Guidance |
|-------|----------|
| `time_bounds` | `not_before`, `not_after`, `max_duration` as applicable. Sets retry/idempotency expectations. |

## Execution identities

| Field | Guidance |
|-------|----------|
| `execution_identities` | Allow list of ids **and** roles (primary, failover, verifier). Exactly one primary acts per step unless contract defines coordination. |

Bind **before** first privileged action; stable for the run; child steps trace to root `execution_id`.

## Mutation and resources

| Field | Guidance |
|-------|----------|
| `allowed_paths` | Prefixes only; narrowest practical. Empty ⇒ no path writes unless ops explicitly allow a non-file channel only. |
| `forbidden_paths` / `exclusions` | High-value paths always denied; **wins** over overlapping allows. |
| `allowed_operations` | Enumerate: `read`, `write`, `delete`, `exec`, `api_call`, `send_message`, etc. **`delete` and `exec` are never implied by `write`.** |

## Side effects (mutations)

| Field | Guidance |
|-------|----------|
| `side_effect_channels` | List every external channel or `none` explicitly. Email, webhooks, tickets, vendor APIs = channels. |
| `side_effect_limits` | Caps: recipients, create count, rate, dry-run phase, idempotency keys, notification suppression. |

Undeclared channel ⇒ **denied**.

## Blast radius and rollback

| Field | Guidance |
|-------|----------|
| `blast_radius` | One repo, one branch, one env, one namespace—**named**, not “everything.” |
| `rollback` | Optional; steps or automation if verification fails; who approves rollback. |

## Success and verification

| Field | Guidance |
|-------|----------|
| `success_criteria` | Objective checklist; include evidence types (diff stats, test output, message ids). |
| `verification` | Automated commands, CI jobs, human sign-off; prefer verifier independence for high risk. |

**No success claim** until criteria are met with evidence.

## Stop and escalate

| Field | Guidance |
|-------|----------|
| `stop_conditions` | Ambiguity, test failure, limit exceeded, revocation, need for undeclared op—**halt without “done”.** |
| `escalation` | Channel, role, SLA; payload includes `task_id`, `execution_id`, what was tried, facts—not silent retry with wider scope. |

## Handoff and dependencies

| Field | Guidance |
|-------|----------|
| `handoff` | For Type **C**: from identity, to identity, artifact name, acceptance check. |
| `dependencies` | Other `task_id`s that must finish first. |

## Audit

| Field | Guidance |
|-------|----------|
| `audit` | What to log (commands, diffs, API ids), retention if relevant. |

---

**Check:** If you cannot fill `success_criteria`, `verification`, and `stop_conditions`, the contract is incomplete—treat as Type **D**.
