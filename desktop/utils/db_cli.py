"""Terminal DB inspector for the desktop app.

Provides an interactive CLI to:
- show DB summary (path, size, tables, row counts)
- view table rows
- delete the database file with confirmation

Intended to be invoked from desktop/main.py when --cli is passed.
"""

import os
from typing import Iterable

from app.config import DB_FILE
from infra.db import get_connection


def _human_size(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{int(size)} B"


def _print_kv(title: str, items: Iterable[tuple[str, str | int]]):
    print(f"\n{title}")
    print("-" * len(title))
    for k, v in items:
        print(f"{k:>16}: {v}")


def _list_tables() -> list[str]:
    with get_connection() as conn:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        return [row[0] for row in cur.fetchall()]


def _count_rows(table: str) -> int:
    with get_connection() as conn:
        cur = conn.execute(f"SELECT COUNT(*) FROM {table}")
        return int(cur.fetchone()[0])


def _print_rows(table: str, limit: int = 50):
    with get_connection() as conn:
        cur = conn.execute(f"SELECT * FROM {table} LIMIT ?", (limit,))
        rows = cur.fetchall()
        if not rows:
            print(f"\nTable '{table}' is empty.")
            return
        columns = rows[0].keys()
        print(f"\n{table} (showing up to {limit} rows)")
        print("-" * (len(table) + 22))
        print(" | ".join(columns))
        print("-" * 80)
        for r in rows:
            print(" | ".join(str(r[c]) for c in columns))


def _show_summary():
    exists = DB_FILE.exists()
    size = DB_FILE.stat().st_size if exists else 0
    tables = _list_tables() if exists else []
    _print_kv(
        "Database",
        [
            ("Path", str(DB_FILE)),
            ("Exists", "Yes" if exists else "No"),
            ("Size", _human_size(size)),
        ],
    )
    print("\nTables and row counts")
    print("---------------------")
    if not tables:
        print("(no tables)")
    else:
        for t in tables:
            try:
                print(f"{t:>16}: {_count_rows(t)}")
            except Exception as e:
                print(f"{t:>16}: error: {e}")


def _delete_db():
    if not DB_FILE.exists():
        print(f"No database file at {DB_FILE} to delete.")
        return
    print(f"\nAbout to delete: {DB_FILE}")
    confirm = input("Type DELETE to confirm: ").strip()
    if confirm == "DELETE":
        try:
            os.remove(DB_FILE)
            print("Database file deleted.")
        except Exception as e:
            print(f"Failed to delete: {e}")
    else:
        print("Cancelled.")


def run_cli():
    print("CircleSync DB Inspector")
    print("=======================")
    while True:
        print(
            "\nOptions:\n"
            "  1) Summary (path, size, table counts)\n"
            "  2) View table rows\n"
            "  3) Delete database file\n"
            "  0) Exit\n"
        )
        choice = input("Select: ").strip()
        if choice == "1":
            _show_summary()
        elif choice == "2":
            if not DB_FILE.exists():
                print(f"Database file not found at {DB_FILE}.")
                continue
            tables = _list_tables()
            if not tables:
                print("No tables found.")
                continue
            print("Available tables:", ", ".join(tables))
            t = input("Table name (or 'all'): ").strip()
            if t.lower() == "all":
                for tbl in tables:
                    _print_rows(tbl)
            elif t in tables:
                try:
                    lim_s = input("Limit rows (default 50): ").strip()
                    lim = int(lim_s) if lim_s else 50
                except ValueError:
                    lim = 50
                _print_rows(t, limit=lim)
            else:
                print("Unknown table.")
        elif choice == "3":
            _delete_db()
        elif choice == "0":
            break
        else:
            print("Unknown selection. Try again.")
