#!/usr/bin/env python3
"""Copy the shared skill into a client's personal or project skills folder."""
import argparse
from pathlib import Path
import shutil
import sys

SOURCE = Path(__file__).resolve().parents[1] / "skills/saas-builder"
CLIENT_DIRS = {"codex": ".codex", "claude-code": ".claude", "cursor": ".cursor"}


def install(client, scope="user", project_dir=None, dry_run=False, home=None):
    if scope == "project":
        if project_dir is None:
            raise ValueError("--project-dir is required for project scope")
        root = Path(project_dir).expanduser().resolve()
        if not root.is_dir():
            raise ValueError("Project directory must already exist")
    else:
        if project_dir is not None:
            raise ValueError("--project-dir requires --scope project")
        root = Path(home) if home is not None else Path.home()
    destination = root / CLIENT_DIRS[client] / "skills/saas-builder"
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Skill already exists; compare it before replacing: {destination}")
    if not dry_run:
        # copytree's default dirs_exist_ok=False also rejects a concurrent install.
        shutil.copytree(SOURCE, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", required=True, choices=CLIENT_DIRS)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        destination = install(args.client, args.scope, args.project_dir, args.dry_run)
    except (OSError, ValueError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        return 1
    print(f"{'Would install to' if args.dry_run else 'Installed to'}: {destination}")
    if not args.dry_run:
        print("Start a new client session and confirm SaaS Builder is available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
