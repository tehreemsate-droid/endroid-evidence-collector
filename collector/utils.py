from pathlib import Path
import subprocess

# ✅ UPDATE THIS if your adb is somewhere else:
ADB_PATH = str(Path.home() / "Downloads" / "platform-tools-latest-windows" / "platform-tools" / "adb.exe")

def adb_cmd(*args: str) -> list[str]:
    return [ADB_PATH, *args]

def run(cmd: list[str], timeout: int = 90) -> tuple[int, str, str]:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()