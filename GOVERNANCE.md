# Governance: adopting Contract-First Systems for tools and agents

This document explains **how** organizations (or solo operators) can adopt the standard: **new tools** declare what they *could* do; **supervisors** grant what they *may* do for each task. It avoids vendor lock-in: “tool” means any program or agent that acts on the world, including shell scripts, CI, or model-driven runtimes.

---

## 1. Roles in adoption

| Role | Responsibility |
|------|-----------------|
| **Standard owner** | Maintains `docs/standard.md`, templates, and schema; bumps version on breaking changes. |
| **Tool author** | Publishes a **capability manifest** for the tool (see below). |
| **Supervisor** | Issues or approves **task contracts** that reference capabilities at **subset** of what the tool supports; **matches or creates** a **concrete execution identity** (expertise, boundary, resources) **before** execution; **delegates** all **mutable** work to that identity; monitors boundaries through the run. Operates as **control plane** by default: **does not** **directly** **mutate** **reality** (files, services, side-effecting APIs, data, messages, credentials, infrastructure, persistent state) in lieu of a **bound** **executor** except under a documented **execution bridge** when **unavoidable** (`docs/standard.md` §1.1). **Does not** treat executor or tool **self-report** as sufficient proof of success—**verifies** against the contract (see §3 and README “Why this is the backbone”). |
| **Verifier** | Human or system that enforces `success_criteria` consistently with **independent** evidence (not trust-by-default on executor “done” claims). |
| **Operator** | Ensures runtimes can enforce or **detect** contract violations and produce **violation records**. |

Adoption is incremental: you can start with **human-supervised** contracts in tickets before any automation enforces them.

---

## 2. How new tools should declare capabilities

Each tool (or each **major** version) should ship a **capability manifest** that answers, in machine- or human-readable form:

1. **Standard version** — Which Contract-First Systems version the manifest targets (e.g. `1.0`).  
2. **Operations** — The full set of `allowed_operations` the tool is capable of (not what *this* run may use).  
3. **Path / resource model** — Whether the tool touches local files, which roots it expects, and whether it can be confined to prefixes.  
4. **Side channels** — All external systems it can contact (APIs, email, webhooks) and under what *generic* use cases.  
5. **Identity support** — How the tool **labels** its runs (`task_id`, `execution_id` in env vars, log fields, or HTTP headers) and whether it can carry an **identity profile** (display name, visual marker, expertise/domain, boundary summary) alongside those ids.  
6. **Idempotency and retries** — How duplicate requests are recognized or not.  
7. **Enforcement** — Whether the tool can **self-limit** to a supplied contract, or only **report** what it did for post-hoc checks.

**Example shape (illustrative YAML fragment):**

```yaml
tool: "example-ticket-tool"
contract_first_standard: "1.0"
max_operations: ["read", "api_call"]
side_channels:
  - api:issues.internal/v2  # project-scoped; tool accepts allowed_projects list at runtime
identity:
  log_fields: [task_id, execution_id]
  header_injection: false  # central proxy adds headers
```

The manifest is **not** a contract by itself. It is the **ceiling** of what the tool *can* be asked to do when correctly configured.

---

## 3. How supervisors grant limited authority

1. **Start from a template** — `templates/task-spec.md` and `examples/` for the class of work.  
2. **Subset the manifest** — The contract’s `allowed_operations`, `allowed_paths`, and `side_effect_channels` are **intersections** with the org’s need, not the tool’s full power.  
3. **Name identities** — List allowed `execution_id` patterns or service accounts, not “any user.” For each task, **record identity selection**: use an **existing** profile that fits the needed **expertise/domain** and **boundary**, or **create** a new named identity before execution; document **why** (`identity_selection` in schema / task template).  
4. **Checkpoint boundaries** — For longer or multi-step work, require **anti-blur checkpoints** so scope and tool permissions do not drift; if expertise no longer matches, **stop** and re-issue contract or identity—do not expand ad hoc.  
5. **Tie verification to evidence** — Define what "green" means before execution starts. **Acceptance** requires **evidence** aligned with that definition—**not** the executor’s summary alone. Supervisors (or **verifiers**) **check** diffs, **automation/CI status**, **side effects** against the contract, and **commit/message metadata** when repo or release work is in scope. **Executor claims require verification**; repeated misses **harden** contracts, checklists, or hooks.  
6. **Version and supersede** — If scope must grow, issue a new `task_id` with `supersedes` to preserve audit chain.

**Grant least privilege:** the default is **tight**; loosen only when a concrete step fails under verification (then **new** contract, not on-the-fly permission expansion).

7. **Control plane vs actuator** — Supervisors and **orchestrators** **define** and **approve**; **executors** **change** the world under **contract**. If your platform conflates the two, **separate** **identities** and **forbid** **supervisor**-path **mutations** in policy, or require **`direct_execution_policy`** / **`execution_bridge`** fields (`docs/standard.md` §2.1) so ad hoc “I’ll just do it” is **visible** and **rare**. **Read-only** **verification** by the supervisor remains **in** **bounds** when the **contract** allows; **implementation** and **side effects** **must not** be **smuggled** in as “verification” without a **bridge**.

---

## 4. Runtime integration patterns

- **Pre-flight check** — Before running, a wrapper validates a JSON/ YAML contract against `schemas/task-contract.schema.json` and local policy (e.g. allowed org-wide prefixes).  
- **Inject binding** — Pass `task_id` and `execution_id` as environment variables; reject runs without them in sensitive environments.  
- **Post-hoc scan** — If the tool cannot self-limit, a scanner checks diffs, API audit logs, or message logs against the contract; failures → **violation record**.  
- **CI gate** — Merge only if verification commands match the **exact** `success_criteria` in the contract attached to the PR.

No single pattern fits all; pick based on what you can enforce honestly.

---

## 5. Multi-tool and multi-agent environments

- **One contract per task**; multiple executors use **handoff** and **dependencies** (see `docs/standard.md`).  
- **No shared “god” key** — Each tool account only has the API scopes needed for its manifest; the contract **narrows** further per task.  
- **Conflict** — If two tools could touch the same resource, the supervisor assigns **lock** or **phase split** in the contract so verification remains unambiguous.

---

## 6. Evolving the standard

- **Non-breaking** changes: new optional fields, new examples, clarifications.  
- **Breaking** changes: new required fields or stricter rules → bump `version` in `docs/standard.md` and `schemas/`.  
- **Changelog** — Keep a short `CHANGELOG.md` in this repo if the standard owner needs history (optional; not required for first adoption).

---

## 7. Summary

**Tools** declare **capabilities**; **supervisors** issue **task contracts** that are strict subsets, **delegate** **mutable** work to **bound** **executors** (or **document** a rare **execution bridge**), and **verify-before-acceptance** so **success** is **evidence-backed**, not self-reported; **verifiers** enforce **success**; **violation records** make **failure**, **overreach**, and **supervisor** **direct**-**mutation** **without** a **bridge** **legible**. That loop is the governance **backbone** for safer tool and agent ecosystems—without mandating a single product or cloud.
