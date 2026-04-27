# Practical problems solved: before and after

This document is **implementation-adjacent**: each section names a class of real failure, shows what usually goes wrong **without** contracts, and what **contract-first** behavior looks like. Examples are concrete enough to copy into your own runbooks.

---

## 1. Repository modification

**Failure mode without contracts**

- A general instruction (“clean up the API layer”) leads an executor to touch **ten** modules, rename public types, and “improve” error messages project-wide. Reviewers see a 3k-line diff; some changes are good, some break downstream consumers; **nobody** agreed to a public API change.
- Branch discipline collapses: work lands on `main` by mistake, or long-lived branches merge conflict explosions.
- **Traceability** is lost: it is unclear which automated run produced which commit.

**Safer behavior with contracts**

- The contract states: **one repository**, **one branch** (or a named feature branch), **path globs** such as `src/api/v2/**` only, and **exclusions** for `package-lock.json` and generated code unless listed.
- `allowed_operations` includes `write` and `read` but not `delete` unless a deletion sub-task is approved.
- `success_criteria` requires: unit tests for package X pass, no new compiler warnings, diff under N lines *or* explicit waiver in a **new** contract.
- The **execution identity** is in commit metadata or CI job name: `task=AUTH-123`, `execution=claude-001`.
- On ambiguity (“should we bump semver?”), the executor **stops** and **escalates** instead of choosing.

---

## 2. Infrastructure and service changes

**Failure mode without contracts**

- “Fix the health check” becomes a config edit on the wrong cluster, or a **shared** load balancer change that affects multiple teams.
- Terraform or Helm applies run **without** a maintenance window, causing restarts in peak hours.
- Rollback is undefined: partial apply leaves **drift** nobody tracks.

**Safer behavior with contracts**

- `blast_radius` names **one** environment (e.g. `staging` first), then a **separate** follow-up contract for `production` with stricter verification.
- `allowed_paths` in infra-as-code terms = specific stack directory or `*.tf` under `infra/apps/payments/`.
- `time_bounds` include maintenance window; executor refuses apply outside the window.
- `success_criteria`: health endpoint returns 200, synthetic check passes, **and** `terraform plan` is empty after apply (or recorded exception with supervisor sign-off).
- `rollback` is a named script or `helm rollback` step if verification fails **within T minutes**.

---

## 3. Email, messaging, and API side effects

**Failure mode without contracts**

- A script “notifies the team” by blasting an **all@** list or the wrong **Slack** channel, including partial debug output.
- An integration posts to a **public** API without dry-run, creating duplicate **tickets** or **charges**.
- **Idempotency** is ignored: the same event fires five times, sending five near-identical messages.

**Safer behavior with contracts**

- `side_effect_channels` lists exactly: `email:team-foo`, `api:issue-tracker#create`, and **not** `email:all-company` unless explicitly allowed.
- `side_effect_limits` cap recipients, set **dry_run: true** for first run, or require **two-person** approval for external customer email.
- `success_criteria` may require: one message id returned, stored in the audit log; or “zero messages sent” for dry-run validation task.
- **Stop** if the tool cannot prove **recipient list** matches allow list after resolution (groups expanded to members for audit only in controlled tools).

---

## 4. File cleanup and deletion

**Failure mode without contracts**

- “Remove old logs” uses `rm -rf` on a path that **symlinks** to something critical, or deletes **this year’s** archives by misparsed dates.
- Valuable user uploads live under a “temp” prefix by historical accident.

**Safer behavior with contracts**

- `allowed_paths` for deletion are **minimal prefixes**; `exclusions` list known-good anchors (`/data/keep/**`).
- The contract requires **listing** (dry run) and **size/count** expectations before **actual** delete in a two-phase **subcontract** or explicit checklist step.
- `success_criteria`: disk usage below X, **and** no files newer than **cutoff** deleted (verified by a script with defined behavior).
- **Execution identity** for destructive runs is a **dedicated** id with no write access elsewhere—reduces blast if credentials leak.

---

## 5. Multi-executor workflows

**Failure mode without contracts**

- Two agents (or a human and an agent) edit the same files concurrently; last writer wins, tests go red.
- Handoff is verbal: “I’ll let the other bot handle the merge”—no **artifact** or **lock**.
- **Partial** completion is invisible: one executor thinks the job is “mostly done” and hands off a broken tree.

**Safer behavior with contracts**

- `dependencies` order tasks: **contract B** may not start until **task A** is verified.
- `handoff` includes: **artifact** (branch name, tarball, ticket state), **from** / **to** identity, and **acceptance** criteria for the receiving executor.
- **Single writer** per resource: contract specifies **lock** (branch, file, or ticket state machine) for the covered paths.
- Each phase has its **own** `task_id` and `verification`; the pipeline only advances when the prior verifier passes.

---

## Summary

| Domain | Uncontracted risk | Contract lever |
|--------|------------------|-----------------|
| Code | API drift, huge diffs | Paths, op allow list, success tests |
| Infra | Wrong env, no rollback | Blast radius, windows, rollback |
| Comms | Wrong audience, spam | Channel allow list, limits, dry-run |
| Deletion | Wrong tree, no dry-run | Narrow paths, two-phase, exclusions |
| Multi-agent | Races, vague handoff | Dependencies, handoff, single writer |

These patterns are **boring** on purpose. Boredom in operations is how you keep **blast radius** small and **audit** possible.
