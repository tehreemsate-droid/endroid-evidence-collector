from pathlib import Path
from .utils import run, adb_cmd

def collect_device_info(out_dir):
    out_dir = Path(out_dir)
    output_file = out_dir / "device_info.txt"

    rc, out, err = run(adb_cmd("shell", "getprop"), timeout=60)

    if rc != 0 or not out:
        output_file.write_text(
            f"ERROR collecting device info:\n{err}",
            encoding="utf-8",
            errors="ignore"
        )
        return {"device_info": str(output_file), "error": True}

    output_file.write_text(out, encoding="utf-8", errors="ignore")
    return {"device_info": str(output_file)}