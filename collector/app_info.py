from pathlib import Path
from .utils import run, adb_cmd

def collect_app_info(package: str, out_dir):
    out_dir = Path(out_dir)
    output_file = out_dir / "app_info.txt"

    rc, out, err = run(adb_cmd("shell", "dumpsys", "package", package), timeout=120)

    if rc != 0 or not out:
        output_file.write_text(
            f"ERROR: Could not collect app info for {package}\n\n{err}",
            encoding="utf-8",
            errors="ignore"
        )
        return {"app_info": str(output_file), "error": True}

    # Quick highlights (optional)
    highlights = []
    keys = ["versionName=", "versionCode=", "codePath=", "dataDir=", "installerPackageName="]
    for line in out.splitlines():
        s = line.strip()
        for k in keys:
            if k in s and s not in highlights:
                highlights.append(s)

    content = []
    content.append(f"# package: {package}")
    content.append("\n# highlights")
    content.extend(highlights if highlights else ["(no highlights found)"])
    content.append("\n# full dumpsys package output (trimmed?)")
    content.append(out)

    output_file.write_text("\n".join(content), encoding="utf-8", errors="ignore")
    return {"app_info": str(output_file)}