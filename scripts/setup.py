#!/usr/bin/env python3
"""Rasterize — Cross-platform setup script.

Creates a virtual environment via pdm and installs all rendering engines.

Usage:
    python scripts/setup.py          # Full setup with pdm
    python scripts/setup.py --bare   # Pip install into current env (no pdm)
"""

import subprocess
import sys
import os
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PACKAGES = [
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


def run(cmd, description, check=True):
    """Run a command and print status."""
    print(f"  {description}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"  WARNING: {description} failed: {result.stderr[:200]}")
        return False
    return True


def setup_with_pdm():
    """Set up using pdm (creates venv automatically)."""
    if not shutil.which("pdm"):
        print("pdm not found. Installing pdm...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "pdm", "--user"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"  Failed to install pdm: {result.stderr[:200]}")
            print("  Install manually: python -m pip install pdm --user")
            print("  Or run with --bare to install into the current environment.")
            sys.exit(1)
        print("  pdm installed successfully.\n")

    print("=== Rasterize: Setting up with pdm ===\n")

    print("[1/3] Installing dependencies into venv...")
    result = subprocess.run(
        ["pdm", "install"], cwd=REPO_ROOT, capture_output=True, text=True
    )
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


def setup_bare():
    """Install packages directly into the current Python environment."""
    print("=== Rasterize: Installing into current Python environment ===\n")

    python = sys.executable

    print(f"[1/3] Installing packages with {python}...")
    result = subprocess.run(
        [python, "-m", "pip", "install"] + PACKAGES,
        capture_output=True, text=True,
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


def main():
    if "--bare" in sys.argv:
        setup_bare()
    else:
        setup_with_pdm()


if __name__ == "__main__":
    main()
