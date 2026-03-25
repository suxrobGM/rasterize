# Setup & Installation

All engines are managed through pdm, which creates an isolated virtual
environment automatically.

## Install all engines at once

```bash
# If pdm is not installed: python -m pip install pdm --user
pdm install                              # creates venv + installs all deps
pdm run playwright install chromium      # browser binary for Playwright engine
```

## Or run the setup script

```bash
python scripts/setup.py          # auto-installs pdm if missing, then all engines
python scripts/setup.py --bare   # skip pdm, install into current Python env
```

## Running scripts

Always use `pdm run python` to execute generation scripts so they use
the plugin's venv:

```bash
pdm run python generate_card.py
```

## Checking engine status

```bash
pdm run python scripts/check_engines.py            # show status
pdm run python scripts/check_engines.py --install   # install missing engines
```
