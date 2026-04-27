# Execution identity — template

**Standard version:** 1.0 (see `docs/standard.md`)

An **execution identity** is the named, bound actor that carries out a `task_id`. It exists so every action is traceable to a declared identity—not to “the assistant” in the abstract. The **supervisor** must **match or create** this identity **before** execution, per §3 of the standard.

---

## Identity presentation

| Field | Value |
|-------|--------|
| `execution_id` | Stable id for this run, e.g. `exec-20260427-001` |
| **Display name** | Human-meaningful label, e.g. `Jarvis — docs-only executor` |
| **Emoji / color** | Visual marker for operators (emoji, hex color, or team convention token) |

## Expertise and boundary

| Field | Value |
|-------|--------|
| **Expertise / domain** | What this identity is authorized to reason about and touch for **this** task (e.g. “Markdown docs in repo X only”) |
| **Communication style** | How this identity reports (e.g. terse bullets, full traces, structured JSON)—so reviewers know what to expect |
| **Precise execution boundary** | One explicit paragraph: **in scope** vs **out of scope** for this identity on this task—must not blur into unrelated “helpfulness” |

## Binding

| Field | Value |
|-------|--------|
| `task_id` | Must match the active task contract. |
| `parent_execution_id` | (Optional) if subordinate to a coordinator run. |
| `bound_at` | ISO 8601 |
| `bound_by` | Supervisor or automated binder id |

## Declared role

| Field | Value |
|-------|--------|
| `role` | e.g. `primary executor`, `verifier`, `read-only probe` |
| `runtime` | e.g. `local shell`, `ci:job-name`, `agent-framework-vX` |

## Resources (aligned with contract)

**Authority is only what the contract allows.** Lists here are a **snapshot for operators**; the contract remains source of truth.

| Field | Value |
|-------|--------|
| **Allowed resources** | Path prefixes, APIs, tools, accounts this identity may use on this run |
| **Forbidden resources** | Explicit denies (must include high-value paths even if also in contract `exclusions`) |

## Stop, escalation, non-sharing

| Field | Value |
|-------|--------|
| **Stop conditions** | When **this** identity must halt without claiming success (ambiguity, boundary insufficient, missing access, limit hit) |
| **Escalation** | Where to send stops: channel, role, SLA; payload must include `task_id`, `execution_id`, facts—no silent widen-scope retries |

**Non-sharing**

- This identity must **not** act on other tasks without a new contract or documented `handoff`.
- This identity is **revoked** when: (copy from contract or state “supervisor revoke / contract expiry: …”)

## Authority snapshot (contract mirror)

Summarize for log clarity (not a second source of truth):

- Allowed path prefixes: 
- Allowed operations: 
- Side channels: 

## Attribution

**How this id appears in logs, commits, or job metadata:**  
- e.g. Git trailer `Contract-Task: TASK-…`, `Execution-Id: …`

---

**Signature / system bind:** `________` **Date:** `________`
