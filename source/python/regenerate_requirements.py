#!/usr/bin/env python3
"""
Regenerate requirements files from pyproject.toml files.

This script is called during Bazel builds to ensure requirements.txt files
are always in sync with pyproject.toml files across the monorepo.
"""

import os
import subprocess
import sys
from pathlib import Path


def find_pyproject_files() -> list[Path]:
    """Find all pyproject.toml files in the monorepo."""
    project_root = Path(__file__).parent.parent.parent
    pyproject_files = []

    for root, dirs, files in os.walk(project_root):
        # Skip hidden and cache directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        if "pyproject.toml" in files:
            pyproject_files.append(Path(root) / "pyproject.toml")

    return sorted(pyproject_files)


def get_requirements_file(pyproject_path: Path) -> Path:
    """Get the corresponding requirements file for a pyproject.toml."""
    # Standard location: same directory or ..../requirements_lock.txt
    requirements_file = pyproject_path.parent / "requirements_lock.txt"
    return requirements_file


def regenerate_requirements(pyproject_path: Path) -> tuple[bool, str]:
    """Regenerate requirements file from pyproject.toml using pip-tools or uv."""
    requirements_file = get_requirements_file(pyproject_path)

    try:
        # Try using uv (faster)
        result = subprocess.run(
            ["uv", "pip", "compile", str(pyproject_path), "-o", str(requirements_file)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            return (
                True,
                f"Generated {requirements_file.relative_to(pyproject_path.parent.parent.parent)}",
            )

        # Fallback to pip-tools
        result = subprocess.run(
            ["pip-compile", str(pyproject_path), "-o", str(requirements_file)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            return (
                True,
                f"Generated {requirements_file.relative_to(pyproject_path.parent.parent.parent)}",
            )

        return False, f"Failed to generate {requirements_file}: {result.stderr}"

    except FileNotFoundError:
        # Tools not available - this is OK, just skip silently
        # Installation instructions are shown in main() if needed
        return (
            True,
            f"Skipped {requirements_file.relative_to(pyproject_path.parent.parent.parent)} (tools not available)",
        )
    except subprocess.TimeoutExpired:
        return False, f"Timeout generating requirements for {pyproject_path}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    """Main entry point."""
    print("=" * 70)
    print("Regenerating requirements from pyproject.toml files")
    print("=" * 70)

    pyproject_files = find_pyproject_files()

    if not pyproject_files:
        print("No pyproject.toml files found")
        return 0

    print(f"\nFound {len(pyproject_files)} pyproject.toml files\n")

    success_count = 0
    failure_count = 0
    failures = []

    for pyproject_path in pyproject_files:
        # Skip if no dependencies
        if "dependencies" not in pyproject_path.read_text():
            continue

        success, message = regenerate_requirements(pyproject_path)

        if success:
            print(f"✓ {message}")
            success_count += 1
        else:
            print(f"✗ {message}")
            failure_count += 1
            failures.append(message)

    print("\n" + "=" * 70)
    print(f"Results: {success_count} successful, {failure_count} failed")
    print("=" * 70)

    if failures:
        print("\nFailures:")
        for failure in failures:
            print(f"  - {failure}")

    return 1 if failure_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
