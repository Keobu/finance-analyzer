"""Launch the Streamlit dashboard without the onboarding prompt."""

from __future__ import annotations

import pathlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / ".streamlit"
CONFIG_PATH = CONFIG_DIR / "config.toml"
CREDENTIALS_PATH = CONFIG_DIR / "credentials.toml"


def prepare_streamlit_home() -> None:
    """Ensure Streamlit uses the project-local config directory."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text("[browser]\ngatherUsageStats = false\n")
    if not CREDENTIALS_PATH.exists():
        CREDENTIALS_PATH.write_text("[general]\nemail = \"\"\n")

    # Monkey-patch Path.home so Streamlit stores credentials within the repo.
    pathlib.Path.home = classmethod(lambda cls: ROOT)  # type: ignore[assignment]


def main() -> None:
    prepare_streamlit_home()

    from streamlit.web import bootstrap

    flag_options = {
        "server.headless": False,
        "browser.gatherUsageStats": False,
    }

    try:
        bootstrap.run(str(ROOT / "app.py"), False, [], flag_options)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
