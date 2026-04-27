# Task types A–D

Classify every contract-requiring task. Type drives **granularity**, **handoff rules**, and **when to refuse execution**.

## Type A — single known operation

**Definition:** One logical action with a clear verb and resource (e.g. “add trailing newline to `config/foo.yaml`”, “run read-only `lint` and report”).

**Behavior:**

- Contract still lists `allowed_paths`, `allowed_operations`, and `success_criteria`—brief but explicit.
- Verification is usually one command or observable.
- **Stop** if the single action expands into “while we’re here” edits.

## Type B — bounded multi-step

**Definition:** Several steps, same domain, finite scope (e.g. “fix failing tests in package X”, “migrate config key in three files”).

**Behavior:**

- Include implicit **step budget** or explicit milestones in `success_criteria`.
- Re-read contract between steps; check revocation.
- **Stop** when the next step needs paths, ops, or channels not listed—escalate for new contract.
- Prefer incremental verification (per-step or per-PR).

## Type C — multi-domain or handoff workflow

**Definition:** Multiple executors, services, or approval gates; work crosses ownership boundaries (e.g. app change + infra ticket + security review).

**Behavior:**

- Define **`handoff`**: artifact, recipient identity, acceptance criteria.
- **Separate contracts** per phase if blast radius or verifier independence requires it.
- Coordinator identity must not impersonate worker authority; workers bind only to their contract.
- **Stop** at handoff boundaries until the next contract or acceptance is explicit.

## Type D — unclear, dangerous, or under-specified

**Definition:** Missing target env, account, data classification, rollback story, or success definition; or instruction implies high blast radius without limits; or policy says “delegate” but execution target is wrong.

**Behavior:**

- **Do not mutate or cause side effects.** Read-only clarification is ok if within policy.
- Produce a **gap list** (bullet points) and **escalate** to `supervisor` path.
- If partial info exists, propose a **tight Type A/B** contract for a **probe** (read-only or dry-run only) as a separate explicit task—never “just try it.”

## Quick decision rules

1. More than one **independent** owner or runtime ⇒ **C**.
2. More than **three** file areas or **two** distinct side-effect channels ⇒ at least **B**, often **C**.
3. Any **production** or **irreversible** path without named blast radius and rollback ⇒ **D** until filled.
4. **Delegation** without named `execution_identities` ⇒ **D**.

## Type × mutation default

| Type | Default posture |
|------|-----------------|
| A | Minimal allow lists; single verification gate |
| B | Tight paths; stop between steps |
| C | Per-phase contracts or explicit `handoff`; no cross-identity borrowing |
| D | No mutation; escalate |
