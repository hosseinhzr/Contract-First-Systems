---
name: contract-first-delegation
description: Use when delegating work to another executor, mutating repos or data, causing external side effects (API, email, tickets), running destructive or infra-changing commands, coordinating multiple executors, or when authority or scope is ambiguous—before acting, bind identity and write a bounded task contract.
---

# Contract-first delegation

Operate under **no implicit authority**: if it is not in the contract, it is not allowed.

## Orchestrator / supervisor: control plane, not executor

**Default posture:** act as the **main orchestrator** or **supervisor**—**not** as the hand that **mutates** the world. The supervisor **defines intent**, **writes or approves** **task contracts**, **selects or creates** **bound execution identities**, **delegates** all work that **changes** durable or externally visible state, **monitors** **boundaries**, **verifies** outputs **against the contract** **before acceptance**, and **records** **violations**. The supervisor is the **control plane**; **executors** (other agents, jobs, humans, or tool runtimes) are the **actuators** under contract.

- **Do not touch mutable reality directly** as the supervisor path: no direct **files**/**repos**/**services**/**APIs (side-effecting)**/**databases**/**messages**/**credentials**/**infrastructure**/**persistent state** when that action should run under a **bound execution identity**—**delegate** it.
- **Mutable execution** belongs to a **bound** identity and **task contract**; the supervisor does **not** self-execute those steps in **normal** operation.
- **Read / inspect** for **verification** is allowed when the **contract** and **policy** allow (including dry-runs where non-mutating). That is **not** a license to perform **implementation** or **side effects** the contract assigns to an **executor**.
- **Exception — execution bridge** only if **no** suitable executor exists and direct action is **unavoidable**: require a **written** spec, **narrow** scope, **explicit** mutation **permission**, **rollback/containment**, **verification**, and **immediate** **revocation** of **elevated** access **after** completion. **Direct** action **without** a bridge when one is required is a **violation**.

Alignment: `docs/standard.md` §1.1, `templates/task-spec.md` (supervisor role separation), optional fields `supervisor_role`, `direct_execution_policy`, `execution_bridge` in `schemas/task-contract.schema.json`.

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
2. **Expert identity first (supervisor step)** — Before any privileged action, decide: does an **existing** named execution identity have the right **expertise/domain** and **declared boundary** for this task? If **yes**, use it and record **why** it fits. If **no** and execution is required, **define and bind a new** concrete identity **first**: stable `execution_id`, **display name**, **emoji/color** (or equivalent marker), **expertise/domain**, **communication style**, **precise execution boundary**, **allowed/forbidden resources**, **stop conditions**, and **escalation** for boundary mismatch. Never run as a vague “agent” with an unstated boundary.
3. **Draft the contract** using field guidance in `references/contract-fields.md` (mirror org templates if available). Include `identity_selection` (use_existing vs create_new + rationale) and `boundary_monitoring` checkpoints when the run is multi-step or long-lived.
4. **Bind execution identity** — exactly **one** primary `execution_id` (and alternates only if the contract lists them). Declare it in messages, logs, or metadata **before** the first privileged action. No identity borrowing. **Every** action maps to **one** identity and its boundary; if the work outgrows that boundary, **stop** and **escalate**—do not silently expand tool permissions or scope.
5. **Permission** — default **read-only**. **Mutation** (including **all** side-effect channels) must appear under `allowed_operations`, `allowed_paths`, and/or `side_effect_channels` with limits. Unlisted = denied. Do not grant **ad hoc** tool access step-by-step; align with the identity’s allowed resources and the contract.
6. **Scope guards** — set `allowed_paths`, `exclusions`, `side_effect_limits`, `blast_radius`, `stop_conditions`, `escalation`, `verification`, and `success_criteria`. Prefer narrowest prefixes; exclusions win over broad allows.
7. **Boundary checkpoints** — During execution, re-state the active identity, its boundary, and contract limits at planned checkpoints (and before irreversible or external side effects). If expertise or boundary no longer matches the work, **stop** and obtain a matching identity or new contract.
8. **Execute** only inside the contract. If you hit ambiguity, missing access, or a limit: **stop**, do not finish with unrelated edits.
9. **Verify** against `success_criteria` and the `verification` plan **before** claiming success. Failed verification ⇒ not done; rollback or new contract. **As supervisor or delegate:** **never** accept another executor’s “done” on **self-report alone**—**you** (or a designated **verifier** process) must **independently** check **evidence** (diff, artifacts, test/CI **status**, **side effects**, **commit** message/metadata as applicable) against the **task contract**. Executor claims are **useful** but **untrusted** until **checked**; **success = evidence that matches the contract**, not a narrative. **Repeated** drift ⇒ **harden** the contract, tooling, or checklists in `templates/task-spec.md`.
10. **Violations and closure** — If a **violation is detected** (boundary breach, forbidden action, unauthorized mutation, false-completion risk, supervisor overreach without bridge, repeated drift, etc.), you **must** file a **structured** violation record **before** closing, accepting, or signing off the task or review. **Do not** treat an empty template folder or informal chat as compliance. Link each `violation_id` to the task (see `violation_records` in `schemas/task-contract.schema.json`). If you are the supervisor or verifier, **block** closure until records exist—same bar as verify-before-acceptance. Details: `references/violation-records.md`, `templates/violation-record.md`, `docs/standard.md` §8.

## Roles

- **Supervisor** — approves contract; **matches or creates** execution identity before execution; **delegates** mutable work to **bound** **executors**; keeps boundaries explicit and monitored; **verifies** outcomes against the contract **before acceptance** (diff, status, artifacts, side effects, commit metadata as relevant—**not** trust-by-default on executor self-report); **does not** accept or close a task when a **violation was detected** until **linked** structured violation record(s) are **filed** (§8 closure gate); can revoke; receives escalations; does not silently substitute scope or blur identity boundaries. **Does not** act as default **actuator** for **mutable** work (no **direct** “touching” **reality** in normal mode—**control plane**, not **executor**; see **Orchestrator / supervisor** above and execution **bridge** when unavoidable).
- **Executor** — declares identity, acts only within contract, runs declared checks, records violations; does not expand its own authority; does **not** expect blind trust for completion claims.

If **policy** states execution must be delegated (e.g. production changes via a specific pipeline), **do not** bypass with direct local action—obtain the right executor and contract.

## Normative alignment

If this skill is vendored alongside **Contract-First Systems**, field names and rules map to `docs/standard.md` and `templates/` at the repository root. The references below are sufficient when those files are not present.

## References

- `references/task-types.md` — A/B/C/D behavior and checklists.
- `references/contract-fields.md` — how to fill each contract section.
- `references/violation-records.md` — when and how to record breaches.
- `references/worked-examples.md` — repo change, API/side effect, deletion, multi-executor handoff.
