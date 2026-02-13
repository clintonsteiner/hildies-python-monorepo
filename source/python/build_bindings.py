#!/usr/bin/env python3
"""
Build script for Hildie Python bindings.

Supports building Rust (PyO3), Go (ctypes), and C++ (ctypes) bindings.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


class BindingsBuilder:
    """Builds Python bindings for Rust, Go, and C++ components."""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent
        self.bindings_dir = self.repo_root / "source/hildie/bindings"
        self.go_dir = self.repo_root / "source/hildie/go"
        self.cpp_dir = self.repo_root / "source/hildie/cpp"
        self.lib_dir = self.bindings_dir / "python/hildie_bindings/lib"

    def run(self, cmd, cwd=None, description=""):
        """Run a command and handle errors."""
        if description:
            print(f"\n{'=' * 70}")
            print(f"  {description}")
            print(f"{'=' * 70}")

        print(f"$ {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=cwd)

        if result.returncode != 0:
            print(f"❌ Error: {description or ' '.join(cmd)}")
            return False

        print(f"✅ Success: {description or ' '.join(cmd)}")
        return True

    def build_rust(self):
        """Build Rust bindings with PyO3."""
        print("\n" + "=" * 70)
        print("  BUILDING RUST BINDINGS (PyO3)")
        print("=" * 70)

        # Check if maturin is installed
        result = subprocess.run(["python3", "-m", "pip", "show", "maturin"], capture_output=True)

        if result.returncode != 0:
            print("Installing maturin...")
            if not self.run(
                ["python3", "-m", "pip", "install", "maturin"], description="Install maturin"
            ):
                return False

        # Build Rust bindings
        return self.run(
            ["maturin", "develop"], cwd=self.bindings_dir, description="Build Rust PyO3 bindings"
        )

    def build_go(self):
        """Build Go bindings with ctypes."""
        print("\n" + "=" * 70)
        print("  BUILDING GO BINDINGS (ctypes)")
        print("=" * 70)

        # Check if Go is installed
        result = subprocess.run(["go", "version"], capture_output=True)
        if result.returncode != 0:
            print("❌ Go is not installed. Please install Go 1.21+")
            return False

        # Create lib directory
        self.lib_dir.mkdir(parents=True, exist_ok=True)

        # Build Go shared library
        lib_file = "libhildie_go.so"
        if sys.platform == "darwin":
            lib_file = "libhildie_go.dylib"
        elif sys.platform == "win32":
            lib_file = "libhildie_go.dll"

        lib_path = self.go_dir / lib_file

        if not self.run(
            ["go", "build", "-o", lib_file, "-buildmode=c-shared", "./..."],
            cwd=self.go_dir,
            description=f"Build Go shared library ({lib_file})",
        ):
            return False

        # Copy to bindings location
        dest = self.lib_dir / lib_file
        try:
            shutil.copy(lib_path, dest)
            print(f"✅ Copied {lib_file} to {dest}")
            return True
        except Exception as e:
            print(f"❌ Error copying {lib_file}: {e}")
            return False

    def build_cpp(self):
        """Build C++ bindings with ctypes."""
        print("\n" + "=" * 70)
        print("  BUILDING C++ BINDINGS (ctypes)")
        print("=" * 70)

        # Determine output filename
        lib_file = "libhildie_cpp.so"
        if sys.platform == "darwin":
            lib_file = "libhildie_cpp.dylib"
        elif sys.platform == "win32":
            lib_file = "libhildie_cpp.dll"

        lib_path = self.cpp_dir / lib_file

        # Create lib directory
        self.lib_dir.mkdir(parents=True, exist_ok=True)

        # Find compiler
        compiler = shutil.which("g++") or shutil.which("clang++")
        if not compiler:
            print("❌ C++ compiler not found (g++ or clang++)")
            return False

        # Build C++ shared library
        cmd = [compiler, "-shared", "-fPIC", "-std=c++17", "-o", lib_file, "hildie.cpp"]

        if not self.run(
            cmd, cwd=self.cpp_dir, description=f"Build C++ shared library ({lib_file})"
        ):
            return False

        # Copy to bindings location
        dest = self.lib_dir / lib_file
        try:
            shutil.copy(lib_path, dest)
            print(f"✅ Copied {lib_file} to {dest}")
            return True
        except Exception as e:
            print(f"❌ Error copying {lib_file}: {e}")
            return False

    def build_all(self):
        """Build all bindings."""
        results = {
            "Rust (PyO3)": self.build_rust(),
            "Go (ctypes)": self.build_go(),
            "C++ (ctypes)": self.build_cpp(),
        }

        print("\n" + "=" * 70)
        print("  BUILD SUMMARY")
        print("=" * 70)

        for name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status}  {name}")

        all_passed = all(results.values())

        print("\n" + "=" * 70)
        if all_passed:
            print("✅ All bindings built successfully!")
            print("\nUsage:")
            print("  from hildie_bindings import greet_rust, add_rust")
            print("  from hildie_bindings import greet_go, add_go")
            print("  from hildie_bindings import process_data, compute_factorial")
        else:
            print("❌ Some bindings failed to build")
        print("=" * 70 + "\n")

        return all_passed


def main():
    parser = argparse.ArgumentParser(description="Build Hildie Python bindings")
    parser.add_argument("--rust", action="store_true", help="Build Rust (PyO3) bindings only")
    parser.add_argument("--go", action="store_true", help="Build Go (ctypes) bindings only")
    parser.add_argument("--cpp", action="store_true", help="Build C++ (ctypes) bindings only")
    parser.add_argument("--all", action="store_true", help="Build all bindings (default)")

    args = parser.parse_args()

    builder = BindingsBuilder()

    # Default to all if nothing specified
    if not (args.rust or args.go or args.cpp or args.all):
        args.all = True

    success = True

    if args.all:
        success = builder.build_all()
    else:
        if args.rust:
            success = builder.build_rust() and success
        if args.go:
            success = builder.build_go() and success
        if args.cpp:
            success = builder.build_cpp() and success

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
