"""Launch the Streamlit dashboard via a subprocess for local use."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / ".streamlit"
CONFIG_PATH = CONFIG_DIR / "config.toml"
CREDENTIALS_PATH = CONFIG_DIR / "credentials.toml"


def prepare_environment() -> dict[str, str]:
    """Prepare environment variables and config files before launching Streamlit."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text("[browser]\ngatherUsageStats = false\n")
    if not CREDENTIALS_PATH.exists():
        CREDENTIALS_PATH.write_text("[general]\nemail = \"\"\n")

    env = os.environ.copy()
    env.setdefault("STREAMLIT_CONFIG_DIR", str(CONFIG_DIR))
    env.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")
    env.setdefault("STREAMLIT_SUPPRESS_EMAIL_PROMPT", "true")
    env.setdefault("HOME", str(ROOT))
    return env


def main() -> None:
    env = prepare_environment()
    cmd = [
        "streamlit",
        "run",
        str(ROOT / "app.py"),
        "--browser.gatherUsageStats=false",
    ]

    try:
        subprocess.run(cmd, check=True, env=env)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
