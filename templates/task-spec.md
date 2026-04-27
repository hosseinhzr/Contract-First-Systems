# Task contract — template

**Standard version:** 1.0 (see `docs/standard.md`)

---

## Supervisor role separation and execution bridge

The **main supervisor** or **orchestrator** is the **control plane** (intent, contract, identity selection, delegation, boundary monitoring, verification, violation recording), **not** the default **actuator** for mutable work. All **mutations** run under a **bound execution identity** and this contract unless an **execution bridge** is active (see `docs/standard.md` §1.1).

| Policy | Choice |
|--------|--------|
| **`direct_execution_policy`** | ☐ `forbidden` — supervisor must **not** mutate files, repos, services, APIs, DBs, messages, credentials, infra, or persistent state except **read/inspect for verification** as allowed below.  ☐ `bridge_only` — any unavoidable direct action only under completed **execution bridge** row.  ☐ `not_applicable` — (e.g. policy encoded outside this template) |

| Execution bridge (only if direct supervisor/orchestrator action is unavoidable) | |
|-------------------------------------------------------------------------------|---|
| **Written task spec or contract addendum** attached / referenced | ☐ |
| **Narrow scope** (minimum mutable surface) | ☐ |
| **Explicit mutation permission** (what, where, until when) | ☐ |
| **Rollback / containment** | ☐ |
| **Verification** steps | ☐ |
| **Immediate role / credential revocation** after completion | ☐ |
| **Justification** (why no bound executor was available) | |

**If `direct_execution_policy` is `forbidden` and no bridge is active:** any direct implementation or side effect by a supervisor process is a **violation** (file per `templates/violation-record.md`).

**Read-only verification** — The supervisor may **read** or **non-mutating inspect** (e.g. diffs, logs, approved dry-runs) to **verify** outcomes, consistent with this contract. That does **not** authorize performing the **executor**’s implementation or side effects outside an **execution bridge** when a bridge is required.

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

### Identity selection (required before execution)

The **supervisor** completes this **before** any privileged action. Execution must not proceed on an unnamed or boundary-vague “agent.”

| Question | Answer |
|----------|--------|
| **Decision** | ☐ Use **existing** allowed identity  ☐ **Create / spawn** new named identity (add to allow list or supersede contract) |
| **Chosen `execution_id`** | |
| **Rationale** | Why this identity’s **expertise/domain** and **declared boundary** fit **this** task (or why a new one was required) |
| **Escalation if mismatch** | If mid-run work exceeds this identity’s boundary: stop, escalate to ________, do not silently expand scope |

Attach a completed `templates/execution-identity.md` per active identity (or equivalent JSON fields).

### Boundary monitoring / anti-blur checkpoints

Long or multi-step work **must** include explicit checkpoints where the executor (or supervisor) re-states: active identity, its boundary, contract `allowed_paths` / `exclusions`, and **non-goals**.

| When (trigger or time) | Checkpoint: restate boundary + limits | Pass / adjust / stop |
|------------------------|----------------------------------------|----------------------|
| e.g. start of session | | |
| e.g. every N steps or 1h | | |
| e.g. before side effects | | |

If a checkpoint reveals **expertise or boundary mismatch**, **stop** and **escalate**; obtain a matching identity or a new contract—do not blur roles.

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

### Supervisor acceptance (verify before close)

**Do not** close the task on **executor self-report alone**. Executors are capable but fallible; treat their summary as **claims** until checked. **Acceptance** means **evidence** matches the contract and `success_criteria` below—not a verbal or chat “done.”

**Supervisor checks (tick when satisfied; note evidence or N/A):**

- [ ] **Scope** — Changed paths/operations match `allowed_paths`, `exclusions`, `allowed_operations`, and `blast_radius`; no **undeclared** work.
- [ ] **Diff / artifacts** — Reviewed (or policy-reviewed) for unintended edits; **artifacts** (builds, exports, etc.) match what verification requires.
- [ ] **Status** — Any required commands, jobs, or tests **executed and passed**; failures not waived without a new contract.
- [ ] **Side effects** — Only **declared** `side_effect_channels` used; **limits** and idempotency respected; no silent extra sends/calls.
- [ ] **Commit & metadata** — If the task includes VCS/PR work: **message**, **body**, **scope of commit(s)**, and **forbidden** lines/trailers (per org policy) are **explicitly** OK.
- [ ] **Contract cross-check** — `success_criteria` items **proven** with the evidence type named in this section—not assumed from executor narrative.

**If the same class of miss recurs,** **tighten** the next contract, checklist, or automation—do not normalize informal acceptance.

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
