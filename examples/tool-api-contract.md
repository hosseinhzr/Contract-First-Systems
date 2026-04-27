# Example: future tool or API integration

**Standard version:** 1.0  
**Fictional** — models how a “tool that calls an API on behalf of the org” would request and operate under a contract, without naming a vendor’s product.

---

## Scenario

An internal **Ticket Bridge** service creates and updates work items in an external **issue system** (REST API). A **supervisor** delegates “sync the release checklist” to a **bounded executor** that must not spam customers or the whole company.

---

## Task contract (filled)

| Field | Value |
|-------|--------|
| `task_id` | `TASK-REL-9x3` |
| `version` | `1.0` |
| `summary` | Create one private ticket; attach release checklist; no emails. |
| `supervisor` | `eng-leads:msingh` |
| `time_bounds` | max_duration: `15m` |

**Intent:** The ticket is for the **eng-release** private project only, with labels `rel-2026.05` and `checklist`, linking to the internal doc URL.

**Non-goals:** No comments on existing tickets, no status transitions on other work items, no public boards.

**Execution identities (allowed):** `tool-ticketbridge-prod#job=REL9x3` only.

**`allowed_paths`:** n/a (no local fs; tool is remote-only).

**`allowed_operations`:** `api_call` (read minimal fields + create issue + attach link).

**`side_effect_channels`:**  
- `api:issues.example.internal/v2` — **create** on project `eng-release` only.  
- `api:issues.example.internal/v2` — **get** for idempotency check on single slug `rel-2026-05-checklist` (if exists, **do not** create duplicate; exit success with id).

**`side_effect_limits`:**  
- Max `create` **1**; max `get` **5**; rate **≤ 1 req/s**.  
- `email:off` (tool must not trigger notification emails via separate integration; if API has `suppress_notifications: true`, use it).

**`success_criteria`:**  
1. Response includes issue id `...` in `eng-release`.  
2. Issue body contains the checklist URL.  
3. No issues created in other projects (verified by project id in response + audit log).

**`verification`:**  
- Tool logs JSON summary to `audit/REL9x3.json` with `issue_id`, `api_request_ids`.  
- Human spot-check: `msingh` confirms ticket visible in `eng-release` only.

**`stop_conditions`:** 401/403, project id mismatch, or **duplicate** detection ambiguous → **stop**, no retries with broader scope.

**`escalation`:** Slack `eng-releases` + page `SRE-rotation` if API unavailable after 3 bounded retries (same `task_id` in `Idempotency-Key` header per vendor pattern).

**`blast_radius`:** One issue in one private project; no mass updates.

**`audit`:** Retain `audit/REL9x3.json` 90 days; include `X-Request-Id` from API in log.

**Supervisor approval:** `msingh` **2026-04-27**

---

## Execution identity (example)

| Field | Value |
|-------|--------|
| `execution_id` | `tool-ticketbridge-prod#job=REL9x3` |
| `task_id` | `TASK-REL-9x3` |
| `role` | primary |
| `runtime` | `ticket-bridge:1.4.0` in locked-down service account `sa-ticketbridge` |

**Attribution:** API `X-Internal-Source` header: `task=TASK-REL-9x3;execution=...` (if your policy allows; otherwise use audit log only).

---

## Contrast: without a contract

The same “create a ticket” request could: pick the default **public** project, @mention a broad list, or retry create five times and open five tickets. The contract’s **`side_effect_channels`**, **limits**, and **idempotency** are what make the tool’s behavior **predictable and auditable**.

---

## Notes for tool authors

- Declare **exactly** which API verbs and resource families you need (`GOVERNANCE.md`).  
- The supervisor can issue a **tighter** contract than your maximum capability.  
- **False completion** (ticket missing from audit) = violation path, not “probably fine.”
