from pathlib import Path
from .utils import run, adb_cmd

SENSITIVE_KEYWORDS = ["password", "token", "bearer", "authorization", "secret", "apikey", "api_key", "session", "cookie"]

def collect_logs(package: str, out_dir):
    out_dir = Path(out_dir)
    output_file = out_dir / "logs.txt"

    # ✅ Don't clear logcat (it may hang on some devices)
    rc, out, err = run(adb_cmd("logcat", "-d", "-v", "time"), timeout=120)
    if rc != 0:
        output_file.write_text(f"ERROR: {err}", encoding="utf-8", errors="ignore")
        return {"logs": str(output_file), "error": True, "hits": []}

    filtered = [line for line in out.splitlines() if package in line]
    text = "\n".join(filtered) if filtered else "(No package-matching logs found)"
    output_file.write_text(text, encoding="utf-8", errors="ignore")

    lower = text.lower()
    hits = sorted({kw for kw in SENSITIVE_KEYWORDS if kw in lower})

    return {"logs": str(output_file), "hits": hits}