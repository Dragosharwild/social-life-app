"""
Application configuration for the Desktop client.

This centralizes paths and feature flags so other layers don't hard-code
filesystem or environment details.
"""

from pathlib import Path

# Root folder for the desktop app (this file lives under desktop/app/)
DESKTOP_ROOT = Path(__file__).resolve().parents[1]

# Runtime data directory (gitignored)
DATA_DIR = DESKTOP_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLite database file path
DB_FILE = DATA_DIR / "circlesync.sqlite"

# Feature flags (simple booleans for now)
FEATURES = {
    "enable_search": True,
}

# UI settings
APP_TITLE = "CircleSync"
