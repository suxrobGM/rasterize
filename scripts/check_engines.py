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


ENGINES = {
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


def check_engine(name, spec):
    """Check if an engine is available. Returns (available, version)."""
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


def install_engine(name, spec):
    """Install a missing engine."""
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


def main():
    do_install = "--install" in sys.argv

    print("Rasterize — Engine Status\n")

    all_ok = True
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
        print(f"\nRun with --install to install missing engines:")
        print(f"  python {sys.argv[0]} --install")


if __name__ == "__main__":
    main()
