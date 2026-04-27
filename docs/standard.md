# Contract-First Systems — Standard (normative)

**Version:** 1.0  
**Status:** implementable — fields and rules are intended to map directly to policy engines, tickets, and review workflows.

This document defines **core principles**, **required contract fields**, **execution identity rules**, the **mutation model**, **blast radius**, **stop/escalation**, **verification**, **violation handling**, and **versioning**. Tools and supervisors **should** treat a task as non-compliant if required fields are missing or contradictory.

---

## 1. Core principles

1. **No implicit authority** — If it is not in the contract, it is not allowed. “Obvious” follow-on work is out of scope.
2. **Expert identity before execution** — Before any privileged step, the **supervisor** (or supervisor-equivalent control plane) **selects or creates** a **concrete named execution identity** whose **declared expertise/domain** and **precise execution boundary** fit the task. Execution must not start on a “generic agent” with an undifferentiated boundary. Every action thereafter maps to **exactly one** such identity and its declared boundary.
3. **Intent ≠ plan ≠ execution** — The contract states **what** must become true. Planning may be internal, but **declared changes** and **verification** are external and checkable.
4. **Mutations are whitelisted, not blacklisted** — Allow lists of paths, operations, and side channels; default deny.
5. **Stoppable** — The contract defines **when to stop** and **when to escalate** without finishing.
6. **Verifiable** — Success is defined so a **verifier** (human or automated) can say pass or fail with evidence.
7. **Violations are first-class** — Breaches and near-misses are recorded in a **violation record**, not only chat logs.
8. **Small blast radius** — Limits on scope, rate, and rollback are part of the contract, not an afterthought.

---

## 2. Required contract fields

A **task contract** must include the following, using the names below or a documented mapping. Optional fields are listed in section 2.1.

| Field | Description |
|-------|-------------|
| `task_id` | Unique id for this task (stable across retries). |
| `version` | Contract schema or standard version (e.g. `1.0`). |
| `summary` | One-line description of the outcome, not a plan. |
| `intent` | Plain-language **goal** (what “good” means for the org). |
| `supervisor` | Accountable party (user id, team, or role) that approved the contract. |
| `time_bounds` | Not-before / not-after / max duration for execution. |
| `execution_identities` | List of allowed **execution identity** ids and roles (or: single primary identity with alternates for failover). |
| `allowed_paths` | Filesystem or resource paths (prefixes) where mutation is allowed; empty means **no** path mutation unless `allowed_operations` explicitly covers a non-file API. |
| `allowed_operations` | Enumerated operations: e.g. `read`, `write`, `delete`, `exec`, `api_call`, `send_message`. |
| `forbidden_paths` or `exclusions` | High-value paths that remain deny even if broad prefixes match. |
| `side_effect_channels` | Declared external channels: email, webhooks, ticket systems, etc.; `none` is explicit. |
| `side_effect_limits` | Per-channel caps: recipients, rate, dry-run requirement. |
| `success_criteria` | Checklist or machine-checkable conditions that must be true to **close** the task. |
| `verification` | How verification runs: commands, human review, sampling; who may sign off. |
| `stop_conditions` | When the executor must halt without claiming success. |
| `escalation` | Where to send ambiguity, failure, or limit hits; must include a **no silent fail** path. |
| `blast_radius` | Declared max impact: e.g. single service, single repo, single env; rollback requirement. |
| `audit` | What must be logged (command lines, diffs, message ids) and retention note if relevant. |

### 2.1 Recommended optional fields

- `dependencies` — Other task ids that must complete first.  
- `handoff` — For multi-executor work: explicit “from identity / to identity / artifact name”.  
- `rollback` — Steps or automated rollback if verification fails.  
- `supersedes` — Prior `task_id` this contract replaces (chain of authority).
- `identity_selection` — Supervisor record: whether an **existing** allowed identity was used or a **new** one was created for this task, with **rationale** (why this identity fits the needed expertise and boundary).  
- `boundary_monitoring` — **Anti-blur checkpoints**: when the supervisor or executor re-states scope, contract limits, and identity boundary during the run (especially long or multi-step work).

---

## 3. Execution identity rules

### 3.1 Supervisor: match, create, then bind

1. **Match before execution** — On receiving a specific task, the supervisor **first** decides whether an **existing** named identity in the allow list has the right **expertise/domain** and **declared boundary** for the work. If **yes**, that identity is the one bound for the run. If **no** suitable identity exists and execution is still required, the supervisor **creates or spawns** a **new** concrete named identity (new `execution_id` and profile) **before** the first privileged action, and adds it to the contract’s allow list (or issues a superseding contract that does).
2. **No vague executor** — “The assistant,” “the agent,” or an unnamed runtime session **does not** satisfy this standard. The active identity must be **named**, **declared**, and **boundary-complete** per §3.2 before execution.
3. **Escalate on mismatch** — If mid-run the work requires expertise, tools, paths, or side channels **outside** the current identity’s declared boundary, the executor must **stop** and **escalate** (and record a **violation** if a limit was crossed). The supervisor must **re-match** identity and contract—not silently stretch the boundary in chat.

### 3.2 Required identity profile (normative)

Each execution identity used for the task **must** declare, in the contract attachment or an `templates/execution-identity.md` (or equivalent) bound to the same `task_id`:

| Element | Requirement |
|---------|-------------|
| **Name** | Stable `execution_id` plus a human-meaningful **display name** (for logs and operator clarity). |
| **Visual marker** | **Emoji and/or color** (or equivalent UI token) so operators can spot the active identity at a glance. |
| **Expertise / domain** | What this identity is **for** (e.g. “docs-only,” “CI read-only probe,” “repo X feature branch edits”). |
| **Communication style** | How this identity reports (e.g. terse log lines, full diff narration)—so reviewers know what to expect. |
| **Precise execution boundary** | A **single explicit** statement of what is in and out of scope for **this** identity on **this** task (not only the global contract—identity boundary must not blur into “whatever helps”). |
| **Allowed / forbidden resources** | Narrow lists aligned with the contract’s `allowed_paths`, `exclusions`, and side channels; identity must not claim broader tool or path rights than the contract. |
| **Stop conditions & escalation** | Identity-level triggers to halt and where to escalate if the boundary is insufficient—aligned with contract `stop_conditions` and `escalation`. |

### 3.3 Continuous boundary monitoring

1. **Non-blur** — The supervisor’s job is to keep boundaries **explicit**, **scoped**, **monitored**, and **non-blurred** for the whole run. Long tasks **should** include scheduled **checkpoints** (see `boundary_monitoring` / task template) where the active identity re-states its boundary and the contract limits.
2. **One identity per action** — Every privileged action **must** map to **exactly one** execution identity and that identity’s declared boundary. Coordinator patterns use explicit child ids or `handoff`; no shadow work under an unnamed session.
3. **Tool permissions** — Tool and API scopes **must** be justified by the contract and the active identity’s allowed resources—not **ad hoc** grants per step. If the tool layer cannot express the contract, treat as **stop** and **escalate**.

### 3.4 Why this matters (non-normative)

This mechanism directly reduces: **wrong executor selection**, **vague “agent” authority**, **scope drift**, **boundary blur** on long tasks, **lost accountability** in multi-executor setups, and **ad hoc tool permissions** that bypass governance.

### 3.5 Executor/runtime rules (existing semantics)

1. **Declaration** — Before acting, the executor (or its runtime) **declares** the execution identity that matches the contract’s allow list and §3.2.
2. **Stability** — The identity id is **stable** for the run; sub-steps may use child ids, but all log lines must be traceable to a root `execution_id`.
3. **No identity borrowing** — One identity must not act on another’s task without a new contract or an explicit `handoff` in an approved follow-on contract.
4. **Attribution** — Logs and version metadata should record `task_id` and `execution_id` where the platform allows (commit trailers, job labels, message headers in internal tools).
5. **Revocation** — If the supervisor **revokes** a contract, identities derived from it **lose authority** immediately; executors must check revocation between steps.

---

## 4. Mutation permission model

1. **Default deny** — Unlisted paths and operations are denied.
2. **Narrowest prefix wins** — If `allowed_paths` and `exclusions` overlap, **exclusions** win.
3. **Destructive ops** require explicit listing — `delete` and `exec` (arbitrary command) are **not** implied by `write`.
4. **Side effects are mutations** — Sending email, opening tickets, or calling external APIs are mutations on **side_effect_channels** and must be listed and limited.
5. **Elevation** — If the work needs broader rights than the contract, the executor must **not** self-expand; it must **stop** and **escalate** with a violation or request for a new contract.

---

## 5. Blast radius constraints

Contracts must state **where impact may appear**:

- **Repository** — one repo, one branch (or named branches), max diff stats if useful.
- **Infrastructure** — named hosts, stacks, or namespaces; not “the cluster” unless truly global and approved.
- **Data** — which stores or tables may be read vs written; production vs staging.

If execution would exceed the declared surface, the executor must **stop** and record **escalation** (and optionally a **violation** if a limit was actually crossed).

---

## 6. Stop and escalation rules

1. **Stop** when: ambiguous instruction, missing access, test failure, limit exceeded, or supervisor revocation.
2. **Do not** “finish anyway” with partial or unrelated changes.
3. **Escalation** payload should include: `task_id`, `execution_id`, what was attempted, error or diff summary, and **proposed** next step—not silent retries with broader scope.
4. **Rate** — If repeated automation triggers (e.g. webhooks) would duplicate work, the contract’s `time_bounds` and idempotency expectations should be set; executor honors **at-most-once** or **retry with same id** as specified.

---

## 7. Verification rules

1. **Same bar every time** — The verifier applies the `success_criteria` and `verification` section, not ad hoc judgment in chat.
2. **Evidence** — Automated checks (tests, lint, policy scans) are preferred; human sign-off is explicit in `verification` when required.
3. **Failure** — If verification fails, the state is **not** “done”; rollback or new contract is required.
4. **Independence** — Where risk is high, the verifier should not be the same unreviewed process that executed (e.g. separate CI job, second human).

---

## 8. Violation handling

1. **Record** — Use `templates/violation-record.md` (or equivalent) for: what limit, what was observed, which identity, timeframe, and **remediation** (revoke, fix forward, new contract).
2. **Severity** — Classify: attempted unauthorized access, success claimed without evidence, overreach, data exposure, etc.
3. **No punishment theater** — Purpose is **audit and policy improvement**; repeated violations trigger **tighter** default contracts, not one-off arguments.
4. **Disclosure** — If policy requires, violations feed security or compliance process as defined by the org (out of band to this spec).

---

## 9. Versioning and evolution

1. **Contract `version` field** — Bumped when **required** fields or semantics change incompatibly.
2. **Add optional fields** without breaking prior validators when possible; document defaults.
3. **Tool capabilities** — Tools declare which standard version and optional features they support (`GOVERNANCE.md`).
4. **Supersession** — New contracts that replace old ones use `supersedes` to keep an audit chain.

---

## 10. Conformance

A **conformant** implementation:

- Rejects or flags tasks missing required fields.  
- Ensures **expert identity selection or creation** occurs **before** execution and that the active identity satisfies §3.2 where the implementation claims full conformance.  
- Binds **execution identity** to **allowed list** in the contract.  
- Enforces **allow lists** for paths, operations, and side channels.  
- Produces or accepts **violation records** in the standard shape.  
- Runs **verification** before marking success.

This standard does not mandate a specific programming language or storage format; JSON with `schemas/task-contract.schema.json` is one valid encoding.
