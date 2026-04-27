# Worked examples

Condensed patterns; adapt ids and paths to your org. Each example includes **before** (failure mode) and **after** (contract-first shape).

---

## 1. Repository change (Type B)

**Before (uncaught risk):** “Fix the bug in checkout” → edits spread to unrelated modules, lockfile churn, skipped tests.

**After — contract sketch:**

- `task_id`: `TASK-ACME-4412`
- `allowed_paths`: `services/cart/**` only; `exclusions`: `**/vendor/**`, generated files unless waived
- `allowed_operations`: `read`, `write` — **not** `delete`
- `side_effect_channels`: `none`
- `success_criteria`: unit tests for cart pass; diff only under `services/cart/`; linter baseline unchanged for that package
- `stop_conditions`: need generated code or API ambiguity → stop, escalate to named supervisor
- `verification`: CI job green on named branch; optional human merge approval
- `execution_identities`: single automation id + optional human hotfix id

**Identity:** Declare `execution_id` in commit trailers or CI labels **before** push.

---

## 2. API / external side effect (Type A/B)

**Before:** “Create a ticket for the release” → wrong project, duplicate tickets, notification spam.

**After — contract sketch:**

- `allowed_operations`: `api_call` only (explicit verbs)
- `side_effect_channels`: one API base; **create** limited to one project id; **get** for idempotency only
- `side_effect_limits`: max 1 create; max N reads; rate cap; `suppress_notifications` if available
- `success_criteria`: response project id matches allow list; issue body contains required link; audit file lists `issue_id` and request ids
- `stop_conditions`: 401/403, wrong project, ambiguous duplicate → stop; no unbounded retries

**Identity:** Tool job id or service principal name in headers/audit only as policy allows.

---

## 3. Deletion / cleanup (Type B or D)

**Before:** “Clean old files” → deletes production assets or far more than intended.

**After — contract sketch:**

- Classify **D** until targets enumerated; then **B** with two-phase verification.
- `allowed_paths`: narrow prefix; `allowed_operations`: `read`, `delete` **only** if explicitly listed
- `side_effect_channels`: `none` or specific backup API if applicable
- `success_criteria`: **listing** step produces path list under size/count bounds; second step deletes only listed paths; post-check confirms absence **only** of those paths
- `rollback`: backups or restore command if defined; else escalate before delete
- `stop_conditions`: listing exceeds cap or unexpected paths appear → **stop**

**Identity:** Separate ids for listing vs delete phases if policy requires separation of duties.

---

## 4. Multi-executor handoff (Type C)

**Before:** Coordinator runs shell commands while “the other agent” edits the same repo without a written boundary—conflicting commits and unclear attribution.

**After — contract sketch:**

- **Contract 1 (planner):** read-only or draft-artifact only; produces `handoff` artifact: spec file + test list.
- **Contract 2 (implementer):** `allowed_paths` from artifact; must not edit artifact unless contract allows.
- `handoff`: from `execution_id` A to B; artifact name; B acknowledges acceptance criteria before writes.
- `stop_conditions`: artifact stale or conflict detected → stop; new handoff or new `task_id`.
- `verification`: independent CI for implementer; planner does not self-approve merge.

**Identity:** A and B **never** share one `execution_id`; no borrowing.

---

## Cross-cutting reminders

- **Read-only default** until `write`/`delete`/`exec`/`api_call` appear in `allowed_operations` with matching resource allow lists.
- **Verify before** “done.”
- On any breach, **violation record** per `violation-records.md`.
