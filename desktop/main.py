"""Desktop entrypoint.

Default: launch the Tkinter GUI.
Optional: `--cli` starts an interactive terminal tool to inspect/delete the DB.
"""

import argparse
import sys


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CircleSync Desktop")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Start interactive DB inspector instead of GUI",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    if args.cli:
        from utils.db_cli import run_cli
        run_cli()
    else:
        from app.main import run
        run()
