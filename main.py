import argparse
from pathlib import Path

from collector.device_info import collect_device_info
from collector.app_info import collect_app_info
from collector.permissions import collect_permissions
from collector.components import collect_components
from collector.logs import collect_logs
from collector.rules import write_report

from datetime import datetime

def now_stamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def main():
    parser = argparse.ArgumentParser(description="Evidence Collector")
    parser.add_argument("--package", required=True, help="Package name")
    parser.add_argument("--out", default="reports", help="Output folder")
    args = parser.parse_args()

    run_dir = Path(args.out) / f"run_{now_stamp()}"
    run_dir.mkdir(parents=True, exist_ok=True)

    module_outputs = {}
    module_outputs["device"] = collect_device_info(run_dir)
    module_outputs["app"] = collect_app_info(args.package, run_dir)
    module_outputs["permissions"] = collect_permissions(args.package, run_dir)
    module_outputs["components"] = collect_components(args.package, run_dir)
    module_outputs["logs"] = collect_logs(args.package, run_dir)

    write_report(run_dir, args.package, module_outputs)

    print("Evidence collected successfully!")

if __name__ == "__main__":
    main()