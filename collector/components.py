from pathlib import Path
from .utils import run, adb_cmd

def collect_components(package: str, out_dir):
    out_dir = Path(out_dir)
    output_file = out_dir / "components.txt"

    rc, out, err = run(adb_cmd("shell", "dumpsys", "package", package), timeout=120)
    if rc != 0 or not out:
        output_file.write_text(f"ERROR: {err}", encoding="utf-8", errors="ignore")
        return {"components": str(output_file), "error": True}

    # best-effort: grab resolver tables
    sections = []
    grab = False
    for line in out.splitlines():
        s = line.strip()
        if "Activity Resolver Table" in s or "Service Resolver Table" in s or "Receiver Resolver Table" in s or "Provider Resolver Table" in s:
            grab = True
            sections.append("\n" + line)
            continue
        if grab:
            sections.append(line)

    output_file.write_text("\n".join(sections) if sections else "(No resolver tables found)", encoding="utf-8", errors="ignore")
    return {"components": str(output_file)}