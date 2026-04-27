# Example: bounded repository work

**Standard version:** 1.0  
**Fictional but realistic** — copy structure, replace names.

---

## Task contract (filled)

| Field | Value |
|-------|--------|
| `task_id` | `TASK-ACME-4412` |
| `version` | `1.0` |
| `summary` | Fix null dereference in checkout flow (`cart_service`). |
| `supervisor` | `platform-oncall:jdoe` |
| `time_bounds` | not_before: `2026-04-28T10:00:00Z`, not_after: `2026-04-28T18:00:00Z`, max_duration: `3h` |

**Intent:** Restore safe handling when `promo_code` is empty; do not change public REST shapes.

**Non-goals:** No dependency major upgrades, no refactors outside `services/cart/`.

**Execution identities (allowed):** `exec-4412-a` (primary automation), `exec-4412-h` (human hotfix, same task).

**`allowed_paths`:**  
- `acme-mono/services/cart/**`  
- `acme-mono/services/cart/tests/**`

**`exclusions`:**  
- `**/vendor/**`  
- `acme-mono/**/go.sum` (unless supervisor waives in writing under new task id)

**`allowed_operations`:** `read`, `write` — not `delete`.

**`side_effect_channels`:** `none`.

**`success_criteria`:**  
1. `go test ./services/cart/...` passes.  
2. Linter: no new issues in `services/cart` (baseline frozen at commit `abc1234`).  
3. Diff touches only files under `services/cart/`.

**`verification`:** CI workflow `cart-pr` on branch `fix/cart-4412` must be green; optional human review for merge by `platform-oncall`.

**`stop_conditions`:** Failing tests, need to touch generated code, or ambiguity about API compatibility → **stop and escalate** to `platform-oncall:jdoe` via `#oncall-platform`.

**`escalation`:** Slack `#oncall-platform`, tag `@jdoe` if SEV ≥ 2 behavior observed.

**`blast_radius`:** Single service package in one repo; no deploy to prod in this task (merge + CI only; deploy is separate `TASK-ACME-4412-prod`).

**`audit`:** PR link, CI run ids, and commit hash recorded in ticket `ACME-4412`.

**Supervisor approval:** `jdoe` **2026-04-27**

---

## Execution identity (example)

| Field | Value |
|-------|--------|
| `execution_id` | `exec-4412-a` |
| `task_id` | `TASK-ACME-4412` |
| `bound_at` | `2026-04-28T10:15:00Z` |
| `bound_by` | `ci:contract-binder@acme` |

**Attribution in commits:** `git` trailers `Task: TASK-ACME-4412` and `Execution-Id: exec-4412-a`.

---

## Why this contract works

- **Path glob** blocks drive-by edits in unrelated services.  
- **No delete** prevents “cleanup” that removes fixtures another team needs.  
- **Stop** when tests require broader edits forces a new approval round.  
- **Blast radius** keeps production deploy out of scope so this task is about **code correctness first**.
