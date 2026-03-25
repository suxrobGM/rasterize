#!/usr/bin/env python3
"""Rasterize: Engine availability checker and installer.

Run this script to verify which engines are available and install
any that are missing.

Usage:
    python check_engines.py          # Check all engines
    python check_engines.py --install # Install missing engines
"""

import importlib
import subprocess
import sys
from collections.abc import Callable
from typing import TypedDict


class EngineSpec(TypedDict, total=False):
    """Specification for a rendering engine."""

    module: str
    verify: Callable[[], object]
    version: Callable[[], str]
    install_args: list[str]
    post_install: list[str]


ENGINES: dict[str, EngineSpec] = {
    "pillow": {
        "module": "PIL",
        "verify": lambda: __import__("PIL.Image", fromlist=["Image"]).new("RGBA", (1, 1)),
        "version": lambda: __import__("PIL.Image", fromlist=["Image"]).__version__,
        "install_args": [sys.executable, "-m", "pip", "install", "Pillow"],
    },
    "cairo": {
        "module": "cairo",
        "verify": lambda: __import__("cairo").ImageSurface(__import__("cairo").FORMAT_ARGB32, 1, 1),
        "version": lambda: __import__("cairo").version,
        "install_args": [sys.executable, "-m", "pip", "install", "pycairo"],
    },
    "matplotlib": {
        "module": "matplotlib",
        "verify": lambda: (__import__("matplotlib").use("Agg"), __import__("matplotlib.pyplot")),
        "version": lambda: __import__("matplotlib").__version__,
        "install_args": [sys.executable, "-m", "pip", "install", "matplotlib", "numpy"],
    },
    "seaborn": {
        "module": "seaborn",
        "verify": lambda: __import__("seaborn"),
        "version": lambda: __import__("seaborn").__version__,
        "install_args": [sys.executable, "-m", "pip", "install", "seaborn", "pandas"],
    },
    "plotly": {
        "module": "plotly",
        "verify": lambda: __import__("plotly.graph_objects", fromlist=["graph_objects"]).Figure(),
        "version": lambda: __import__("plotly").__version__,
        "install_args": [sys.executable, "-m", "pip", "install", "plotly", "kaleido"],
    },
    "playwright": {
        "module": "playwright",
        "verify": lambda: __import__("playwright.sync_api", fromlist=["sync_api"]),
        "version": lambda: __import__("playwright").__version__,
        "install_args": [sys.executable, "-m", "pip", "install", "playwright"],
        "post_install": [sys.executable, "-m", "playwright", "install", "chromium"],
    },
}


def check_engine(name: str, spec: EngineSpec) -> tuple[bool, str]:
    """Check if an engine is importable and functional.

    Imports the module, runs the verify callable to confirm it works,
    and retrieves the version string.

    Args:
        name: Human-readable engine name (e.g. "pillow").
        spec: Engine specification with module, verify, and version callables.

    Returns:
        A tuple of (available, info) where info is the version string
        if available, or the error message if not.
    """
    try:
        importlib.import_module(spec["module"])
        spec["verify"]()
        try:
            version = spec["version"]()
        except Exception:
            version = "unknown"
        return True, version
    except Exception as e:
        return False, str(e)


def install_engine(name: str, spec: EngineSpec) -> bool:
    """Install a missing engine using pip.

    Runs the install command from the spec, then any post-install steps
    (e.g. downloading browser binaries for Playwright).

    Args:
        name: Human-readable engine name.
        spec: Engine specification with install_args and optional post_install.

    Returns:
        True if installation succeeded, False otherwise.
    """
    print(f"  Installing {name}...")
    result = subprocess.run(spec["install_args"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[:200]}")
        return False

    if "post_install" in spec:
        result = subprocess.run(spec["post_install"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  WARNING: post-install step failed: {result.stderr[:200]}")

    print(f"  Installed {name}")
    return True


def main() -> None:
    """Check all engines and optionally install missing ones.

    Pass ``--install`` on the command line to auto-install any engines
    that are not currently available.
    """
    do_install: bool = "--install" in sys.argv

    print("Rasterize — Engine Status\n")

    all_ok: bool = True
    for name, spec in ENGINES.items():
        available, info = check_engine(name, spec)
        if available:
            print(f"  + {name:12s}  v{info}")
        else:
            all_ok = False
            print(f"  - {name:12s}  not available")
            if do_install:
                install_engine(name, spec)

    if all_ok:
        print("\nAll engines ready!")
    elif not do_install:
        print("\nRun with --install to install missing engines:")
        print(f"  python {sys.argv[0]} --install")


if __name__ == "__main__":
    main()
