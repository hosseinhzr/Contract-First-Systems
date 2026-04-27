# Violation records

A **violation** is a crossed limit, attempted unauthorized action, false completion risk, or material near-miss—**not** a normal test failure that stayed inside contract (that is a stop + fix within scope).

## Mandatory before close when detected

If a review, verifier, or supervisor **detects** any situation in **When to record** below, a **structured** record **must** be **filed** and **linked** to the `task_id` **before** the task or review is **accepted** or **closed**. **Do not** skip filing because a template exists in the repo. Conformant tooling **blocks** or **flags** closure when a detected violation has no record (see `docs/standard.md` §8, `violation_policy` / `violation_records` in the task contract schema).

## When to record

Create a structured violation record when **any** of these occur:

- Action outside `allowed_paths`, `allowed_operations`, or `side_effect_channels`.
- Success or “done” communicated without meeting `success_criteria` or skipping `verification`.
- **Identity** mismatch: wrong `execution_id`, borrowing without `handoff`, or acting after revocation.
- **Overreach**: scope creep executed before new approval (even if reverted).
- **Data exposure** risk: logs, artifacts, or messages include data outside `blast_radius` or policy.
- **Elevation attempt**: executor tried to broaden its own authority instead of stopping.
- **Supervisor / orchestrator overreach**: direct mutation of durable or externally visible state without a **bound** executor or without a required **execution bridge** when policy requires one (see `docs/standard.md` §1.1).

Normal **stop_conditions** triggered **without** a breach (e.g. asked to escalate cleanly) ⇒ log for audit if your org requires it, but severity is lower than an overreach violation.

## Severity (examples)

Use consistent labels your org can aggregate:

| Severity | Typical meaning |
|----------|-----------------|
| `attempted_unauthorized` | Tried denied op or path; may or may not have succeeded—assume investigate. |
| `overreach` | Completed or partial change beyond contract. |
| `false_completion` | Reported success without evidence or with failed checks ignored. |
| `data_exposure_risk` | Sensitive data in wrong channel, log, or artifact. |

## Record contents (minimum)

Align fields with `templates/violation-record.md` at repo root when vendored; include at least:

- `violation_id`, `task_id`, `execution_id`, `detected_at`, `detected_by`
- **Rule violated** — quote contract clause or field.
- **Evidence** — diffs, command lines, message ids, API request ids (redact secrets).
- **Severity** (recommended)
- **Containment** — immediate: revoke token, revert commit, block job, notify supervisor.
- **Prevention** — what will reduce recurrence (template, CI, checkpoint).
- **Remediation** — technical fix, process change, new `task_id` for legitimate follow-up.
- `status` — workflow state of the violation record.
- **Verification** — how filing and containment were confirmed.
- **Disclosure** — security/compliance path if required by policy.

Purpose: **audit and policy improvement**, not blame theater. Repeated patterns ⇒ tighter default contracts and tooling checks.

## Containment order of operations

1. **Stop** further privileged actions from the same run if still active.
2. **Revoke** or invalidate credentials/session per playbook.
3. **Revert** or patch forward only under a **new** contract if original cannot be salvaged.
4. **Notify** supervisor via `escalation` path with structured payload.
5. **Preserve evidence** per `audit` rules for investigation.

## Rollback

- If contract defined `rollback`, follow it.
- If not defined, **do not invent** destructive rollback; escalate with options and impact.

## Prevention (follow-up)

- Tighten templates for this task class (narrower paths, mandatory dry-run for deletes).
- Add automated policy checks (CI, admission hooks) where violations repeated.
- For Type **C**, improve `handoff` clarity so identities cannot drift.
