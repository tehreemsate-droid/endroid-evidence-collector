import json
from pathlib import Path

def write_report(out_dir, package: str, module_outputs: dict):
    out_dir = Path(out_dir)

    findings = []

    # Rule: keywords in logs
    hits = module_outputs.get("logs", {}).get("hits", [])
    if hits:
        findings.append({
            "id": "LOG-001",
            "title": "Potential sensitive keywords in logs",
            "severity": "HIGH",
            "evidence": {"keywords": hits, "file": "logs.txt"}
        })

    # Rule: remind review exported components
    if (out_dir / "components.txt").exists():
        findings.append({
            "id": "COMP-REVIEW",
            "title": "Review exported components / intent exposure",
            "severity": "MEDIUM",
            "evidence": {"file": "components.txt"}
        })

    report = {
        "package": package,
        "artifacts": module_outputs,
        "findings": findings
    }

    (out_dir / "findings.json").write_text(json.dumps(report, indent=2), encoding="utf-8")