#!/usr/bin/env python3
"""
Package the Employer Edition (Version A) for delivery.

This script creates a distributable archive that includes ONLY:
  - Compiled Python bytecode (.pyc) — NOT source code
  - Templates and static assets
  - The employer license
  - A pre-configured launcher

Usage:
    python editions/employer/package_employer_edition.py [--output-dir ./dist]
"""

import argparse
import compileall
import os
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Files/dirs to INCLUDE in employer package (as .pyc, not .py)
CORE_MODULES = [
    "agent_dashboard_v2.py",
    "auth_manager.py",
    "credential_manager.py",
    "database.py",
    "portal_automation_agent.py",
    "license_manager.py",
    "core/__init__.py",
    "core/edition.py",
]

INCLUDE_DIRS = [
    "templates",
]

INCLUDE_FILES = [
    "requirements.txt",
    "LICENSE-EMPLOYER",
    "editions/employer/run.py",
    "editions/employer/config.py",
]

# Files that must NEVER be in the employer package
NEVER_INCLUDE = {
    "LICENSE",               # full proprietary license (your eyes only)
    "COPYRIGHT_HEADER.py",
    "PRODUCT_ROADMAP_V2.md",
    "doc/saas-product-guide.html",
    "doc/technical-design.html",
    "editions/commercial",
    ".env",
    ".env.example",
    "agent_config.json",
    "credentials_index.json",
    "users.json",
    "portal_agent.db",
}


def package(output_dir: Path):
    build_dir = output_dir / "AutomatePortal-Employer"

    # Clean previous build
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)

    print(f"Packaging Employer Edition to: {build_dir}")

    # 1. Compile core modules to .pyc and copy bytecode only
    pyc_dir = build_dir / "lib"
    pyc_dir.mkdir()
    for mod_path in CORE_MODULES:
        src = PROJECT_ROOT / mod_path
        if not src.exists():
            print(f"  SKIP (missing): {mod_path}")
            continue

        # Compile
        compileall.compile_file(str(src), force=True, quiet=1)

        # Find the .pyc in __pycache__
        cache_dir = src.parent / "__pycache__"
        pyc_files = list(cache_dir.glob(f"{src.stem}.cpython-*.pyc"))
        if not pyc_files:
            print(f"  WARN: no .pyc found for {mod_path}")
            continue

        # Copy .pyc with clean name
        dest_subdir = pyc_dir / str(Path(mod_path).parent)
        dest_subdir.mkdir(parents=True, exist_ok=True)
        dest = dest_subdir / f"{src.stem}.pyc"
        shutil.copy2(pyc_files[0], dest)
        print(f"  Compiled: {mod_path} -> {dest.relative_to(build_dir)}")

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
        'os.environ["AUTOMATEPORTAL_EDITION"] = "employer"\n'
        'sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))\n'
        'from run import main\n'
        'main()\n'
    )
    print(f"  Created: start.py")

    # 5. Create zip archive
    archive = shutil.make_archive(str(build_dir), "zip", output_dir, build_dir.name)
    print(f"\nPackage ready: {archive}")
    print(f"Directory:     {build_dir}")
    print(f"\nIMPORTANT: This package contains ONLY compiled bytecode.")
    print(f"           Source code is NOT included.")


def main():
    parser = argparse.ArgumentParser(description="Package AutomatePortal Employer Edition")
    parser.add_argument("--output-dir", default="./dist", help="Output directory")
    args = parser.parse_args()

    package(Path(args.output_dir))


if __name__ == "__main__":
    main()
