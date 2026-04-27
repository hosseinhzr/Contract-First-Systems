# Contract-First Systems

A **portable standard** for delegating work to executors (human operators, automations, or agents) under explicit, enforceable **task contracts**. The goal is to replace open-ended “do the thing” instructions with **bounded intent**, **named execution identities**, **mutation limits**, and **verifiable outcomes**—so tools and control planes can grant **least authority** and contain failure.

This repository documents the model, provides templates, and offers examples. It is **not tied to a single vendor**; you can map contracts onto your own supervisor, policy engine, or review workflow.

---

## The problem with unconstrained execution

When a tool or agent runs without a contract, common failures appear:

- **Vague authority** — “fix the bug” can mean edit one file, refactor the module, or rewrite half the service.
- **Scope creep** — the executor “helps” by changing adjacent systems nobody approved.
- **Uncontrolled mutation** — writes land in prod configs, shared secrets, or customer data with no pre-declared surface.
- **No accountability** — logs say “an automation ran” but not *which identity*, *under which limits*, for *which task id*.
- **No stop conditions** — work continues until the model stops typing, not when success criteria are met.
- **Intent mixed with action** — planning, execution, and verification collapse into one opaque step, so bad plans execute immediately and nobody checks the result the same way every time.

Contract-first design addresses these by making **what may happen** and **how we know it worked** as explicit as **what we want**.

---

## The contract-first answer

1. A **supervisor** (human or system) issues a **task contract** before sensitive work: allowed paths, allowed operations, time bounds, and success tests.
2. The **contract** is the source of truth for authority—not chat history, not implicit tool defaults.
3. An **executor** runs only under a declared **execution identity** (a stable name, scope, and parent contract reference).
4. A **verifier** checks outcomes against the contract (automated where possible, human sign-off where required).
5. **Violation records** capture what crossed the line, for audit and policy improvement.

Nothing here requires a specific product; it is a **pattern** you can implement with scripts, policy-as-code, ticket workflows, or agent frameworks.

---

## Architecture

| Component | Role |
|-----------|------|
| **Supervisor** | Creates or approves contracts, binds identities, may halt or escalate. Not the same role as the executor. |
| **Contract** | Declares intent, bounds, allowed mutations, success criteria, stop/escalation rules, and verification hooks. |
| **Executor** | Performs work only within the contract and identity; records actions for traceability. |
| **Verifier** | Asserts that post-state matches success criteria; may be automated, dual-control, or sampled. |
| **Violation record** | Structured report when limits are hit or evidence does not match claims—feeds audit and policy updates. |

Together, these separate **what is requested** (intent in the contract) from **how it is carried out** (execution) and **how we know it is safe to accept** (verification).

---

## Why this is the backbone for future tools and agents

Multi-tool and multi-agent systems fail when every component negotiates ad hoc permissions in natural language. A **contract layer**:

- **Standardizes** how tools **request** capability (pre-declared scopes, not “trust me”).
- **Standardizes** how supervisors **grant** authority in **revocable, auditable** units.
- **Limits blast radius** by construction—contracts say where effects may occur.
- **Makes behavior comparable** across vendors: same fields, same violation semantics, different implementations.

As agents proliferate, the missing piece is not smarter models; it is **governance-shaped interfaces** between control planes and execution.

---

## Before and after: practical scenarios

| Scenario | Without contracts | With contracts |
|----------|-------------------|----------------|
| **Repo change** | Agent edits any file; review is a hope. | Contract lists repo, branch, file glob, and max diff; verifier runs tests + diff gate. |
| **Infra change** | “Deploy fix” might touch five services. | Contract names targets, change type, maintenance window, rollback criteria. |
| **Email/API side effects** | One ambiguous send can go to wrong list. | Contract names recipients, template id, rate cap, and dry-run requirement. |
| **Cleanup** | “Delete old stuff” removes valuable assets. | Contract lists path prefixes, age rule, and mandatory backup/verification step. |
| **Multi-executor** | Two agents race on the same files. | Contracts serialize via task id, branch locks, or explicit handoff fields. |

---

## Quick start: write and use a task contract

1. **Copy** `templates/task-spec.md` and `templates/execution-identity.md`.
2. **Fill** task id, time bounds, allowed paths, allowed operations, **success criteria** (measurable), and **stop/escalation** (when to halt and notify).
3. **Bind** an execution identity: name, parent contract, and scope.
4. **Run** the executor only with those files attached or registered in your supervisor.
5. **Verify** using the same checklist every time; file a **violation record** if limits were crossed.

For machine-readable validation, see `schemas/task-contract.schema.json` and the formal spec in `docs/standard.md`.

**Adoption** for new tools: read `GOVERNANCE.md` for capability declarations and how supervisors grant limited authority.

---

## Repository layout

| Path | Purpose |
|------|---------|
| `docs/standard.md` | Normative standard (principles, fields, rules) |
| `docs/practical-problems-solved.md` | Deep before/after examples |
| `templates/` | Reusable task, identity, and violation templates |
| `examples/` | Worked contract examples |
| `schemas/` | JSON Schema for key contract fields |
| `GOVERNANCE.md` | How to roll this out for tools and agents |

---

## License and use

This standard is provided as **documentation and templates** for implementation in your own systems. Adapt terminology to your org; keep **contracts, identities, verification, and violations** as first-class concepts.
