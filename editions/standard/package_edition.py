#!/usr/bin/env python3
"""
Package the Standard Edition for delivery.

This script creates a distributable archive that includes:
  - Python source files (.py) for customisation
  - Templates and static assets
  - The MIT license
  - A pre-configured launcher

Usage:
    python editions/standard/package_edition.py [--output-dir ./dist]
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Python source files to include
CORE_MODULES = [
    "agent_dashboard_v2.py",
    "auth_manager.py",
    "credential_manager.py",
    "database.py",
    "portal_automation_agent.py",
    "core/__init__.py",
    "core/edition.py",
]

INCLUDE_DIRS = [
    "templates",
]

INCLUDE_FILES = [
    "requirements.txt",
    "LICENSE",
    "editions/standard/run.py",
    "editions/standard/config.py",
    "Dockerfile",
    "docker-compose.yml",
    "entrypoint.sh",
    "test_persistent_profile.py",
]

# Files that must NEVER be in the standard package
NEVER_INCLUDE = {
    "COPYRIGHT_HEADER.py",
    "PRODUCT_ROADMAP_V2.md",
    "DUAL_VERSION_STRATEGY.md",
    "doc/saas-product-guide.html",
    "doc/technical-design.html",
    "editions/commercial",
    "license_manager.py",
    ".env",
    ".env.example",
    "agent_config.json",
    "credentials_index.json",
    "users.json",
    "portal_agent.db",
}


def package(output_dir: Path):
    build_dir = output_dir / "AutomatePortal-Standard"

    # Clean previous build
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)

    print(f"Packaging Standard Edition to: {build_dir}")

    # 1. Copy core Python source files
    for mod_path in CORE_MODULES:
        src = PROJECT_ROOT / mod_path
        if not src.exists():
            print(f"  SKIP (missing): {mod_path}")
            continue

        dest_subdir = build_dir / str(Path(mod_path).parent)
        dest_subdir.mkdir(parents=True, exist_ok=True)
        dest = dest_subdir / src.name
        shutil.copy2(src, dest)
        print(f"  Copied: {mod_path}")

    # 2. Copy template directories as-is
    for dir_name in INCLUDE_DIRS:
        src_dir = PROJECT_ROOT / dir_name
        if src_dir.exists():
            shutil.copytree(src_dir, build_dir / dir_name)
            print(f"  Copied dir: {dir_name}/")

    # 3. Copy allowed files
    for file_path in INCLUDE_FILES:
        src = PROJECT_ROOT / file_path
        if src.exists():
            dest = build_dir / Path(file_path).name
            shutil.copy2(src, dest)
            print(f"  Copied: {file_path}")

    # 4. Write a simple launcher
    launcher = build_dir / "start.py"
    launcher.write_text(
        '#!/usr/bin/env python3\n'
        '"""AutomatePortal - Internal Edition"""\n'
        'import os, sys\n'
        'os.environ["AUTOMATEPORTAL_EDITION"] = "standard"\n'
        'sys.path.insert(0, os.path.dirname(__file__))\n'
        'from run import main\n'
        'main()\n'
    )
    print(f"  Created: start.py")

    # 5. Create zip archive
    archive = shutil.make_archive(str(build_dir), "zip", output_dir, build_dir.name)
    print(f"\nPackage ready: {archive}")
    print(f"Directory:     {build_dir}")
    print(f"\nThis package includes Python source code.")
    print(f"Modify as needed per the MIT license.")


def main():
    parser = argparse.ArgumentParser(description="Package AutomatePortal Standard Edition")
    parser.add_argument("--output-dir", default="./dist", help="Output directory")
    args = parser.parse_args()

    package(Path(args.output_dir))


if __name__ == "__main__":
    main()
