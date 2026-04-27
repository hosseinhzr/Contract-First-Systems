---
name: contract-first-delegation
description: Use when delegating work to another executor, mutating repos or data, causing external side effects (API, email, tickets), running destructive or infra-changing commands, coordinating multiple executors, or when authority or scope is ambiguous—before acting, bind identity and write a bounded task contract.
---

# Contract-first delegation

Operate under **no implicit authority**: if it is not in the contract, it is not allowed.

## When you must pause for a contract

Stop and produce (or obtain) a **task contract** before execution when **any** of these apply:

- **Delegation** — work will be handed to another model, job, human, or tool runtime.
- **Mutation** — filesystem writes, schema/data changes, branch pushes, config edits.
- **External side effects** — HTTP/API calls, email, chat posts, webhooks, ticket creation, payments, provisioning.
- **Destructive or irreversible** — deletes, `DROP`, production toggles, mass refactors, security-sensitive changes.
- **Infrastructure / services** — clusters, hosts, DNS, IAM, pipelines beyond read-only inspection.
- **Multi-executor** — coordinator + workers, handoffs, serial approvals.
- **Ambiguous authority** — unclear which repo, env, account, or role is in scope.

If unsure, treat as contract-requiring and **classify** per `references/task-types.md`.

## Task classification (required)

Label the work **A**, **B**, **C**, or **D** before acting. Classification controls how tight the contract must be and how often you re-check scope.

| Type | Meaning | Contract posture |
|------|---------|------------------|
| **A** | Single known operation | Minimal but still explicit ops + verification |
| **B** | Bounded multi-step | Step budget, stop conditions, per-step verification where useful |
| **C** | Multi-domain or handoff | `handoff` artifacts, separate identities or follow-on contracts |
| **D** | Unclear, dangerous, or under-specified | **Do not execute**; escalate with gaps listed—contract first |

Details: `references/task-types.md`.

## Operating procedure

1. **Classify** the task (A–D). If **D**, escalate; do not broaden scope to “make progress.”
2. **Draft the contract** using field guidance in `references/contract-fields.md` (mirror org templates if available).
3. **Bind execution identity** — exactly **one** primary `execution_id` (and alternates only if the contract lists them). Declare it in messages, logs, or metadata **before** the first privileged action. No identity borrowing.
4. **Permission** — default **read-only**. **Mutation** (including **all** side-effect channels) must appear under `allowed_operations`, `allowed_paths`, and/or `side_effect_channels` with limits. Unlisted = denied.
5. **Scope guards** — set `allowed_paths`, `exclusions`, `side_effect_limits`, `blast_radius`, `stop_conditions`, `escalation`, `verification`, and `success_criteria`. Prefer narrowest prefixes; exclusions win over broad allows.
6. **Execute** only inside the contract. If you hit ambiguity, missing access, or a limit: **stop**, do not finish with unrelated edits.
7. **Verify** against `success_criteria` and the `verification` plan **before** claiming success. Failed verification ⇒ not done; rollback or new contract.
8. **Violations** — if a boundary was crossed or false completion risk exists, file a structured record per `references/violation-records.md`.

## Roles

- **Supervisor** — approves contract, can revoke, receives escalations; does not silently substitute scope.
- **Executor** — declares identity, acts only within contract, verifies, records violations; does not expand its own authority.

If **policy** states execution must be delegated (e.g. production changes via a specific pipeline), **do not** bypass with direct local action—obtain the right executor and contract.

## Normative alignment

If this skill is vendored alongside **Contract-First Systems**, field names and rules map to `docs/standard.md` and `templates/` at the repository root. The references below are sufficient when those files are not present.

## References

- `references/task-types.md` — A/B/C/D behavior and checklists.
- `references/contract-fields.md` — how to fill each contract section.
- `references/violation-records.md` — when and how to record breaches.
- `references/worked-examples.md` — repo change, API/side effect, deletion, multi-executor handoff.
