#!/usr/bin/env python3
"""verify_permanence.py — Run the operational-permanence test citations.

Reads the test-citation fixture at
01_library/library/permanence/test_fixtures/test_citations.json, runs each
URN through the resolver (with test fixtures loaded), and compares the
resolver's response against the expected outcome.

Produces two artifacts:
  - 03_web_app/reports/permanence_audit.json   (machine-readable)
  - 03_web_app/reports/permanence_audit.md     (human-readable)

The verification is the operational counterpart to the constitutional
permanence commitments. A passing run shows that the resolver actually
behaves the way the documents say it must. A failing run is the more
valuable result: it pinpoints where a constitutional promise has not yet
been operationalized.

Usage:
    python 05_scripts/verify_permanence.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "05_scripts"))

from resolve_urn import Resolver  # type: ignore  # noqa: E402

FIXTURE = ROOT / "01_library" / "library" / "permanence" / "test_fixtures" / "test_citations.json"
JSON_OUT = ROOT / "03_web_app" / "reports" / "permanence_audit.json"
MD_OUT = ROOT / "03_web_app" / "reports" / "permanence_audit.md"


def evaluate(citation: dict, response: dict) -> dict:
    """Compare resolver response against a citation's expected outcome."""
    failures = []
    expected_status = citation.get("expected_status")
    actual_status = response.get("resolution_status")
    if expected_status != actual_status:
        failures.append(
            f"resolution_status: expected {expected_status!r}, got {actual_status!r}"
        )
    resolved = response.get("resolved_to") or {}

    if "expected_kind" in citation:
        if resolved.get("kind") != citation["expected_kind"]:
            failures.append(
                f"resolved kind: expected {citation['expected_kind']!r}, "
                f"got {resolved.get('kind')!r}"
            )
    if "expected_layer" in citation:
        if resolved.get("layer") != citation["expected_layer"]:
            failures.append(
                f"layer: expected {citation['expected_layer']!r}, "
                f"got {resolved.get('layer')!r}"
            )
    if "expected_quarantined" in citation:
        if bool(resolved.get("quarantined")) != bool(citation["expected_quarantined"]):
            failures.append(
                f"quarantined: expected {citation['expected_quarantined']!r}, "
                f"got {resolved.get('quarantined')!r}"
            )
    if "expected_lifecycle_state" in citation:
        if resolved.get("lifecycle_state") != citation["expected_lifecycle_state"]:
            failures.append(
                f"lifecycle_state: expected {citation['expected_lifecycle_state']!r}, "
                f"got {resolved.get('lifecycle_state')!r}"
            )
    if "expected_successor" in citation:
        if resolved.get("superseded_by") != citation["expected_successor"]:
            failures.append(
                f"successor: expected {citation['expected_successor']!r}, "
                f"got {resolved.get('superseded_by')!r}"
            )
    if "expected_migration_policy" in citation:
        if resolved.get("migration_policy") != citation["expected_migration_policy"]:
            failures.append(
                f"migration_policy: expected {citation['expected_migration_policy']!r}, "
                f"got {resolved.get('migration_policy')!r}"
            )
    if "expected_redirect_to" in citation:
        # The final resolved URN should match the expected target. The
        # response carries the input_urn (original) and resolved_to.* —
        # the alias-traversed chain gives the final target.
        chain = response.get("aliases_traversed", [])
        final_target = chain[-1].get("new_urn") if chain else None
        if final_target != citation["expected_redirect_to"]:
            failures.append(
                f"alias target: expected {citation['expected_redirect_to']!r}, "
                f"got {final_target!r}"
            )
    if "expected_sub_locator_resolved" in citation:
        sub = resolved.get("sub_locator") or {}
        if bool(sub.get("resolved")) != bool(citation["expected_sub_locator_resolved"]):
            failures.append(
                f"sub_locator.resolved: expected {citation['expected_sub_locator_resolved']!r}, "
                f"got {sub.get('resolved')!r}"
            )

    return {
        "id": citation["id"],
        "urn": citation["urn"],
        "description": citation.get("description", ""),
        "expected_status": expected_status,
        "actual_status": actual_status,
        "passed": not failures,
        "failures": failures,
        "resolver_response": response,
    }


def main() -> int:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    resolver = Resolver(load_test_fixtures=True)

    results = []
    for citation in fixture["test_citations"]:
        response = resolver.resolve(citation["urn"])
        results.append(evaluate(citation, response))

    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    summary = {
        "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fixture": str(FIXTURE.relative_to(ROOT)).replace("\\", "/"),
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "results": results,
    }

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    MD_OUT.write_text(_render_markdown(summary), encoding="utf-8")

    print(f"Wrote {JSON_OUT.relative_to(ROOT)}")
    print(f"Wrote {MD_OUT.relative_to(ROOT)}")
    print(f"Result: {passed}/{total} passed")
    return 0 if passed == total else 1


def _render_markdown(summary: dict) -> str:
    lines: list[str] = []
    lines.append("# Permanence Audit")
    lines.append("")
    lines.append(f"Run at: `{summary['run_at']}`")
    lines.append(f"Fixture: `{summary['fixture']}`")
    lines.append(f"Result: **{summary['passed']}/{summary['total']} passed**")
    lines.append("")
    lines.append(
        "Each test exercises one operational permanence commitment. A failed "
        "test is the more useful kind of result: it names exactly where a "
        "constitutional promise has not yet survived contact with the resolver."
    )
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Id  | URN | Expected | Actual | Pass |")
    lines.append("|-----|-----|----------|--------|------|")
    for r in summary["results"]:
        mark = "OK" if r["passed"] else "FAIL"
        urn = r["urn"].replace("|", "\\|")
        lines.append(
            f"| {r['id']} | `{urn}` | `{r['expected_status']}` | "
            f"`{r['actual_status']}` | {mark} |"
        )
    lines.append("")

    failing = [r for r in summary["results"] if not r["passed"]]
    if failing:
        lines.append("## Failures")
        lines.append("")
        for r in failing:
            lines.append(f"### {r['id']} — `{r['urn']}`")
            lines.append("")
            lines.append(r["description"])
            lines.append("")
            for f in r["failures"]:
                lines.append(f"- {f}")
            lines.append("")
            lines.append("<details><summary>Resolver response</summary>")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(r["resolver_response"], ensure_ascii=False, indent=2))
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    lines.append("## Citations")
    lines.append("")
    for r in summary["results"]:
        lines.append(f"### {r['id']} — `{r['urn']}`")
        lines.append("")
        lines.append(r["description"])
        lines.append("")
        lines.append(f"- Expected status: `{r['expected_status']}`")
        lines.append(f"- Actual status: `{r['actual_status']}`")
        lines.append(f"- Pass: **{'yes' if r['passed'] else 'no'}**")
        lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
