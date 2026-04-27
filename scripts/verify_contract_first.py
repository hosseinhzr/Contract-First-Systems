#!/usr/bin/env python3
"""Mechanical verifier for Contract-First Systems (stdlib only)."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"OK: {msg}")


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)

    required_paths = [
        root / "docs" / "standard.md",
        root / "schemas" / "task-contract.schema.json",
        root / "templates" / "task-spec.md",
        root / "templates" / "execution-identity.md",
        root / "templates" / "violation-record.md",
        root / "examples" / "repo-change-contract.md",
        root / "examples" / "tool-api-contract.md",
        root / "integrations" / "openclaw" / "clawhub" / "contract-first-delegation" / "SKILL.md",
        root / "integrations" / "openclaw" / "clawhub" / "contract-first-delegation"
        / "references"
        / "task-types.md",
        root / "integrations" / "openclaw" / "clawhub" / "contract-first-delegation"
        / "references"
        / "contract-fields.md",
        root / "integrations" / "openclaw" / "clawhub" / "contract-first-delegation"
        / "references"
        / "violation-records.md",
        root / "integrations" / "openclaw" / "clawhub" / "contract-first-delegation"
        / "references"
        / "worked-examples.md",
    ]
    for p in required_paths:
        if not p.is_file():
            fail(f"missing required file: {p.relative_to(root)}")

    schema_path = root / "schemas" / "task-contract.schema.json"
    try:
        with schema_path.open(encoding="utf-8") as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        fail(f"schema is not valid JSON: {e}")

    if schema.get("type") != "object":
        fail("schema root must be type object")

    top_required = set(
        [
            "task_id",
            "version",
            "summary",
            "supervisor",
            "time_bounds",
            "execution_identities",
            "allowed_paths",
            "allowed_operations",
            "success_criteria",
            "verification",
            "stop_conditions",
            "escalation",
            "blast_radius",
            "identity_selection",
            "boundary_monitoring",
            "supervisor_role",
            "direct_execution_policy",
            "execution_bridge",
            "violation_policy",
            "violation_records",
        ]
    )
    got = set(schema.get("required") or [])
    missing = top_required - got
    if missing:
        fail(f"schema root 'required' missing: {sorted(missing)}")
    props = schema.get("properties") or {}
    for k in top_required:
        if k not in props:
            fail(f"schema properties missing top-level field: {k}")

    exec_items = (((props.get("execution_identities") or {}).get("items")) or {})
    id_required = set(
        [
            "execution_id",
            "role",
            "display_name",
            "visual_marker",
            "expertise_domain",
            "communication_style",
            "execution_boundary",
            "allowed_resources",
            "forbidden_resources",
        ]
    )
    id_got = set(exec_items.get("required") or [])
    id_miss = id_required - id_got
    if id_miss:
        fail(f"execution_identities.items.required missing: {sorted(id_miss)}")
    id_props = exec_items.get("properties") or {}
    for k in id_required:
        if k not in id_props:
            fail(f"execution_identities.items.properties missing: {k}")

    norm_paths: list[Path] = [
        root / "docs" / "standard.md",
        schema_path,
        root / "integrations" / "openclaw" / "clawhub" / "contract-first-delegation" / "SKILL.md",
    ]
    for md in sorted((root / "templates").glob("*.md")):
        norm_paths.append(md)
    ref_dir = (
        root / "integrations" / "openclaw" / "clawhub" / "contract-first-delegation" / "references"
    )
    for md in sorted(ref_dir.glob("*.md")):
        norm_paths.append(md)

    corpus = "\n".join(p.read_text(encoding="utf-8") for p in norm_paths)

    checks: list[tuple[str, re.Pattern[str]]] = [
        (
            "control plane + actuator (supervisor vs executor)",
            re.compile(r"control\s+plane", re.I),
        ),
        ("actuator(s) named", re.compile(r"actuator", re.I)),
        (
            "no direct mutable reality / touch mutable",
            re.compile(
                r"(no\s+direct\s+mutable|mutable\s+reality|touch\s+mutable|direct\s+mutable)",
                re.I,
            ),
        ),
        ("execution bridge", re.compile(r"execution\s+bridge|execution_bridge", re.I)),
        (
            "expert / identity before execution",
            re.compile(
                r"(expert\s+identity\s+before|before\s+execution|identity\s+before|match\s+before\s+execution)",
                re.I,
            ),
        ),
        (
            "verify-before-acceptance",
            re.compile(r"verify[-\s]?before[-\s]?acceptance|before\s+acceptance", re.I),
        ),
        (
            "self-report / untrusted until checked",
            re.compile(
                r"(self[-\s]?report|untrusted|until\s+checked|not\s+a\s+substitute|claims\s+until)",
                re.I,
            ),
        ),
        (
            "violation closure gate",
            re.compile(r"closure[-\s]?gate|closure-gated|block.*clos|clos.*accepted", re.I),
        ),
        (
            "structured violation record",
            re.compile(r"structured\s+violation|violation\s+record", re.I),
        ),
        (
            "forbidden commit metadata",
            re.compile(
                r"(forbidden\s+commit|commit\s+metadata|disallowed\s+trailer|commit\s+message)",
                re.I,
            ),
        ),
        (
            "supervisor direct mutation / overreach",
            re.compile(
                r"(supervisor\s+direct|direct\s+mutation|supervisor\s+overreach|direct\s+mutable\s+work)",
                re.I,
            ),
        ),
    ]
    for label, pat in checks:
        if not pat.search(corpus):
            fail(f"normative corpus missing concept ({label})")

    skill_dir = root / "integrations" / "openclaw" / "clawhub" / "contract-first-delegation"
    skill_md = skill_dir / "SKILL.md"
    skill_text = skill_md.read_text(encoding="utf-8")
    if not skill_text.startswith("---"):
        fail("SKILL.md must start with YAML frontmatter")
    fm_end = skill_text.find("---", 3)
    if fm_end == -1:
        fail("SKILL.md frontmatter not closed")
    front = skill_text[3:fm_end]
    if not re.search(r"(?m)^name:\s*contract-first-delegation\s*$", front):
        fail("SKILL frontmatter must include name: contract-first-delegation")
    if not re.search(r"(?m)^description:\s*\S", front):
        fail("SKILL frontmatter must include description:")

    banned_skill_files = {"readme.md", "changelog.md", "installation.md"}
    for entry in skill_dir.iterdir():
        if entry.is_file() and entry.name.lower() in banned_skill_files:
            fail(f"extraneous skill file not allowed: {entry.name}")

    skill_checks = [
        ("delegation identity", re.compile(r"delegat|execution\s+identity|bound\s+identity", re.I)),
        ("verification distrust", re.compile(r"untrusted|independent|self-report|evidence", re.I)),
        ("closure gate", re.compile(r"closure|filed.*before|block.*clos", re.I)),
        ("stop / escalate", re.compile(r"stop.*escalat|escalat", re.I)),
        ("execution bridge", re.compile(r"execution\s+bridge", re.I)),
    ]
    for label, pat in skill_checks:
        if not pat.search(skill_text):
            fail(f"SKILL.md missing expected theme: {label}")

    hook = root / ".git" / "hooks" / "commit-msg"
    if hook.is_file():

        def run_hook(msg: str, *, suppress_stderr: bool = False) -> int:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", suffix=".txt", delete=False
            ) as tf:
                tf.write(msg)
                path = tf.name
            try:
                return subprocess.run(
                    ["/bin/sh", str(hook), path],
                    cwd=str(root),
                    stderr=subprocess.DEVNULL if suppress_stderr else None,
                ).returncode
            finally:
                os.unlink(path)

        bad_rc = run_hook("x\n\nMade-with: Cursor\n", suppress_stderr=True)
        if bad_rc == 0:
            fail("commit-msg hook should reject 'Made-with: Cursor'")
        good_msg = (
            "Jarvis - added contract-first mechanical verifier\n\n"
            "Signed-off-by: Jarvis - added contract-first mechanical verifier\n"
        )
        good_rc = run_hook(good_msg, suppress_stderr=False)
        if good_rc != 0:
            fail("commit-msg hook should accept conformant commit message")
        ok("commit-msg hook rejects Cursor branding and accepts clean message")
    else:
        print(
            "WARNING: .git/hooks/commit-msg not found; skipping hook checks (ok for some clones).",
            file=sys.stderr,
        )

    ok("all contract-first mechanical checks passed")


if __name__ == "__main__":
    main()
