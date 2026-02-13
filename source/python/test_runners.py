#!/usr/bin/env python3
"""
Hildie multi-language test runners.
Provides unified test execution across Python, Java, Go, Rust, and Node.js.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


class TestRunner:
    """Base test runner class."""

    def __init__(self, name: str, timeout: int = 300):
        self.name = name
        self.timeout = timeout
        self.cwd = Path.cwd()

    def run(self) -> tuple[bool, str]:
        """Run the test. Returns (success, output)."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class JavaTestRunner(TestRunner):
    """Run Java tests using javac."""

    def __init__(self):
        super().__init__("Java")
        self.test_dir = Path("source/hildie/java/hildie-java-lib")

    def run(self) -> tuple[bool, str]:
        """Compile and run Java tests."""
        try:
            if not self.test_dir.exists():
                return False, f"Test directory not found: {self.test_dir}"

            os.chdir(self.test_dir)

            # Create bin directory
            bin_dir = Path("bin")
            bin_dir.mkdir(exist_ok=True)

            # Compile
            compile_cmd = [
                "javac",
                "-d",
                "bin",
                "src/main/java/io/hildie/HildieLibrary.java",
                "src/test/java/io/hildie/HildieLibraryTest.java",
            ]

            result = subprocess.run(
                compile_cmd, capture_output=True, text=True, timeout=self.timeout
            )

            if result.returncode != 0:
                return False, f"Compilation failed:\n{result.stderr}"

            # Run
            run_cmd = [
                "java",
                "-ea",
                "-cp",
                "bin",
                "io.hildie.HildieLibraryTest",
            ]

            result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=self.timeout)

            return result.returncode == 0, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return False, f"Test timed out after {self.timeout}s"
        except Exception as e:
            return False, str(e)
        finally:
            os.chdir(self.cwd)


class GoTestRunner(TestRunner):
    """Run Go tests using go test."""

    def __init__(self):
        super().__init__("Go")
        self.test_dir = Path("source/hildie/go")

    def run(self) -> tuple[bool, str]:
        """Run Go tests."""
        try:
            if not self.test_dir.exists():
                return False, f"Test directory not found: {self.test_dir}"

            os.chdir(self.test_dir)

            cmd = ["go", "test", "./..."]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)

            return result.returncode == 0, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return False, f"Test timed out after {self.timeout}s"
        except Exception as e:
            return False, str(e)
        finally:
            os.chdir(self.cwd)


class RustTestRunner(TestRunner):
    """Run Rust tests using cargo."""

    def __init__(self):
        super().__init__("Rust", timeout=600)  # Rust builds can take longer
        self.test_dir = Path("source/hildie/rust")

    def run(self) -> tuple[bool, str]:
        """Run Rust tests."""
        try:
            if not self.test_dir.exists():
                return False, f"Test directory not found: {self.test_dir}"

            os.chdir(self.test_dir)

            cmd = ["cargo", "test", "--all"]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)

            return result.returncode == 0, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return False, f"Test timed out after {self.timeout}s"
        except Exception as e:
            return False, str(e)
        finally:
            os.chdir(self.cwd)


class NodeTestRunner(TestRunner):
    """Run Node.js tests using npm."""

    def __init__(self):
        super().__init__("Node.js")
        self.test_dir = Path("source/hildie/node")

    def run(self) -> tuple[bool, str]:
        """Install dependencies and run tests."""
        try:
            if not self.test_dir.exists():
                return False, f"Test directory not found: {self.test_dir}"

            os.chdir(self.test_dir)

            # Install dependencies
            install_cmd = ["npm", "install", "--silent"]
            result = subprocess.run(
                install_cmd, capture_output=True, text=True, timeout=self.timeout
            )

            if result.returncode != 0:
                return False, f"npm install failed:\n{result.stderr}"

            # Run tests
            test_cmd = ["npm", "test"]
            result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=self.timeout)

            return result.returncode == 0, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return False, f"Test timed out after {self.timeout}s"
        except Exception as e:
            return False, str(e)
        finally:
            os.chdir(self.cwd)


class PythonTestRunner(TestRunner):
    """Run Python tests using bazel."""

    def __init__(self):
        super().__init__("Python")

    def run(self) -> tuple[bool, str]:
        """Run Python tests with bazel."""
        try:
            cmd = ["bazel", "test", "//packages/..."]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)

            return result.returncode == 0, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return False, f"Test timed out after {self.timeout}s"
        except Exception as e:
            return False, str(e)


class TestSuite:
    """Runs all language tests."""

    def __init__(self):
        self.runners = [
            PythonTestRunner(),
            JavaTestRunner(),
            GoTestRunner(),
            RustTestRunner(),
            NodeTestRunner(),
        ]
        self.results = {}

    def run_all(self) -> bool:
        """Run all tests. Returns True if all pass."""
        print("=" * 80)
        print("HILDIE MULTI-LANGUAGE TEST SUITE".center(80))
        print("=" * 80)
        print()

        passed = 0
        failed = 0

        for runner in self.runners:
            print(f"Running {runner.name} tests...")
            success, output = runner.run()

            if success:
                print(f"✅ {runner.name} Tests PASSED")
                passed += 1
            else:
                print(f"❌ {runner.name} Tests FAILED")
                print(f"Output:\n{output}")
                failed += 1

            self.results[runner.name] = (success, output)
            print()

        # Summary
        print("=" * 80)
        total = passed + failed
        if failed == 0:
            print(f"✅ ALL TESTS PASSED ({passed}/{total})".center(80))
            print("BUILD STATUS: SUCCESS ✅".center(80))
        else:
            print(f"❌ SOME TESTS FAILED ({passed}/{total} PASSED)".center(80))
            print("BUILD STATUS: FAILURE ❌".center(80))
        print("=" * 80)

        return failed == 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run Hildie multi-language tests")
    parser.add_argument(
        "--language",
        choices=["python", "java", "go", "rust", "node"],
        help="Run only tests for a specific language",
    )

    args = parser.parse_args()

    suite = TestSuite()

    if args.language:
        # Run only specific language
        runner_map = {
            "python": PythonTestRunner(),
            "java": JavaTestRunner(),
            "go": GoTestRunner(),
            "rust": RustTestRunner(),
            "node": NodeTestRunner(),
        }
        runner = runner_map[args.language]
        success, output = runner.run()
        print(output)
        sys.exit(0 if success else 1)
    else:
        # Run all
        success = suite.run_all()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
