from pathlib import Path
from .utils import run, adb_cmd

def collect_permissions(package: str, out_dir):
    out_dir = Path(out_dir)
    output_file = out_dir / "permissions.txt"

    rc, out, err = run(adb_cmd("shell", "dumpsys", "package", package), timeout=120)

    if rc != 0 or not out:
        output_file.write_text(
            f"ERROR collecting permissions:\n{err}",
            encoding="utf-8",
            errors="ignore"
        )
        return {"permissions": str(output_file), "error": True}

    keep = []
    capture = False

    for line in out.splitlines():
        s = line.strip()

        if s.startswith("requested permissions:") or \
           s.startswith("runtime permissions:") or \
           s.startswith("install permissions:"):
            capture = True

        if capture:
            keep.append(line)

        if capture and s.startswith("Queries:"):
            break

    output_file.write_text(
        "\n".join(keep) if keep else out,
        encoding="utf-8",
        errors="ignore"
    )

    return {"permissions": str(output_file)}