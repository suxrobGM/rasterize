#!/usr/bin/env python3
"""Rasterize — Cross-platform setup script.

Creates a virtual environment via pdm and installs all rendering engines.

Usage:
    python scripts/setup.py          # Full setup with pdm
    python scripts/setup.py --bare   # Pip install into current env (no pdm)
"""

import os
import shutil
import subprocess
import sys

REPO_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Absolute path to the repository root."""

PACKAGES: list[str] = [
    "Pillow",
    "pycairo",
    "matplotlib",
    "seaborn",
    "numpy",
    "pandas",
    "plotly",
    "kaleido",
    "playwright",
]
"""Package names to install for all rendering engines."""


def run(cmd: list[str], description: str, *, check: bool = True) -> bool:
    """Run a subprocess command and print its status.

    Args:
        cmd: Command and arguments to execute.
        description: Human-readable description shown during execution.
        check: If True, print a warning on non-zero exit code.

    Returns:
        True if the command exited successfully, False otherwise.
    """
    print(f"  {description}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"  WARNING: {description} failed: {result.stderr[:200]}")
        return False
    return True


def setup_with_pdm() -> None:
    """Set up the project using pdm.

    Installs pdm if not found, then creates a virtual environment,
    installs all dependencies, downloads the Playwright Chromium binary,
    and verifies engine availability.
    """
    if not shutil.which("pdm"):
        print("pdm not found. Installing pdm...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "pdm", "--user"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  Failed to install pdm: {result.stderr[:200]}")
            print("  Install manually: python -m pip install pdm --user")
            print("  Or run with --bare to install into the current environment.")
            sys.exit(1)
        print("  pdm installed successfully.\n")

    print("=== Rasterize: Setting up with pdm ===\n")

    print("[1/3] Installing dependencies into venv...")
    result = subprocess.run(["pdm", "install"], cwd=REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  pdm install failed: {result.stderr[:300]}")
        sys.exit(1)
    print("  Done.\n")

    print("[2/3] Installing Playwright Chromium browser...")
    subprocess.run(
        ["pdm", "run", "playwright", "install", "chromium"],
        cwd=REPO_ROOT,
    )
    print()

    print("[3/3] Verifying engines...")
    subprocess.run(
        ["pdm", "run", "python", os.path.join("scripts", "check_engines.py")],
        cwd=REPO_ROOT,
    )

    print("\n=== Setup complete! ===")
    print("Run scripts with: pdm run python <script.py>")


def setup_bare() -> None:
    """Install packages directly into the current Python environment.

    Falls back to this mode when pdm is not desired. Installs all engine
    packages via pip, downloads Playwright Chromium, and verifies engines.
    Prints platform-specific hints if pycairo installation fails.
    """
    print("=== Rasterize: Installing into current Python environment ===\n")

    python: str = sys.executable

    print(f"[1/3] Installing packages with {python}...")
    result = subprocess.run(
        [python, "-m", "pip", "install", *PACKAGES],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  pip install failed: {result.stderr[:300]}")
        print("\n  On Windows, pycairo may need prebuilt wheels:")
        print("    pip install pipwin && pipwin install pycairo")
        print("  On Linux/macOS, you may need system packages:")
        print("    sudo apt-get install libcairo2-dev pkg-config python3-dev")
    else:
        print("  Done.\n")

    print("[2/3] Installing Playwright Chromium browser...")
    subprocess.run([python, "-m", "playwright", "install", "chromium"])
    print()

    print("[3/3] Verifying engines...")
    subprocess.run([python, os.path.join(REPO_ROOT, "scripts", "check_engines.py")])

    print("\n=== Setup complete! ===")


def main() -> None:
    """Entry point — dispatch to pdm or bare setup based on CLI args."""
    if "--bare" in sys.argv:
        setup_bare()
    else:
        setup_with_pdm()


if __name__ == "__main__":
    main()
