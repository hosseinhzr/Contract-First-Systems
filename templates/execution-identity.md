# Execution identity — template

**Standard version:** 1.0 (see `docs/standard.md`)

An **execution identity** is the named, bound actor that carries out a `task_id`. It exists so every action is traceable to a declared identity—not to “the assistant” in the abstract.

---

## Binding

| Field | Value |
|-------|--------|
| `execution_id` | Stable id for this run, e.g. `exec-20260427-001` |
| `task_id` | Must match the active task contract. |
| `parent_execution_id` | (Optional) if subordinate to a coordinator run. |
| `bound_at` | ISO 8601 |
| `bound_by` | Supervisor or automated binder id |

## Declared role

| Field | Value |
|-------|--------|
| `role` | e.g. `primary executor`, `verifier`, `read-only probe` |
| `runtime` | e.g. `local shell`, `ci:job-name`, `agent-framework-vX` |

## Authority snapshot

**This identity is allowed only what appears in the contract referenced by `task_id`.**  
Summarize here for log clarity (not a second source of truth):

- Allowed path prefixes: 
- Allowed operations: 
- Side channels: 

## Non-sharing

- This identity must **not** act on other tasks without a new contract or documented `handoff`.
- This identity is **revoked** when: (copy from contract or state “supervisor revoke / contract expiry: …”)

## Attribution

**How this id appears in logs, commits, or job metadata:**  
- e.g. Git trailer `Contract-Task: TASK-…`, `Execution-Id: …`

---

**Signature / system bind:** `________` **Date:** `________`
