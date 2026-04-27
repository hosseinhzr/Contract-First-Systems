# Task contract — template

**Standard version:** 1.0 (see `docs/standard.md`)

---

## Identifiers and accountability

| Field | Value |
|-------|--------|
| `task_id` | `TASK-________________` |
| `version` | `1.0` |
| `summary` | One line: outcome in business terms. |
| `supervisor` | Name or id of approving party. |
| `parent_task_id` | (Optional) if this is a sub-task. |

## Intent

**Goal (intent):**  
What “done” means for the organization, without prescribing implementation.

**Non-goals (explicit):**  
What this task must *not* do.

## Time

| Field | Value |
|-------|--------|
| `not_before` | ISO 8601 or `immediate` |
| `not_after` / deadline | |
| `max_duration` | e.g. `2h` |

## Execution identities

| Identity id | Role | Notes |
|-------------|------|--------|
| | primary | |
| | optional failover | |

## Mutation scope

**`allowed_paths` (prefixes only):**  
- 

**`exclusions` (always deny):**  
- 

**`allowed_operations`:** (check all that apply)  
- [ ] `read`  [ ] `write`  [ ] `delete`  [ ] `exec`  [ ] `other: ________`

## Side effects

**`side_effect_channels`:** `none` or list, e.g. `email:…`, `webhook:…`, `api:…`  
**`side_effect_limits`:** (caps, dry-run first?, idempotency key)  
- 

## Blast radius

**Max impact surface:** (one sentence; e.g. single repo, single service, non-prod only)  
**Environments / clusters / namespaces (if any):**  
- 

## Success criteria (required)

Checklist; must be objectively verifiable.

1. 
2. 
3. 

## Verification

| Aspect | How |
|--------|-----|
| Automated checks | Commands or CI job names |
| Human review | Required? Who? |
| Evidence to retain | e.g. diff, log, message id |

## Stop conditions

When the executor must **halt** (no “success” claim):

- 
- 

## Escalation

| Trigger | Contact / channel | SLA |
|--------|-------------------|-----|
| Ambiguity | | |
| Limit exceeded | | |
| Test failure | | |

## Rollback (if applicable)

- 

## Audit

**Must log / attach:**  
- 

---

**Supervisor approval:** (initials or system id) `________` **Date:** `________`
