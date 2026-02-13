"""Hildie-specific Bazel macros."""

load("@rules_java//java:defs.bzl", "java_binary")
load("@rules_python//python:defs.bzl", "py_binary")

def hildie_cli(name, module):
    """Creates a CLI binary from a hildie module.

    Args:
        name: Binary name (e.g., "hildie-cli")
        module: Module path (e.g., "hildie_cli")
    """
    py_binary(
        name = name,
        srcs = ["source/hildie/{}/main.py".format(module)],
        main = "source/hildie/{}/main.py".format(module),
        deps = ["//:hildie"],
    )

def hildie_java_app(name, main_class, srcs, deps = None):
    """Creates a Java application for hildie.

    Args:
        name: Binary name (e.g., "hildie-java-app")
        main_class: Main class (e.g., "io.hildie.HildieApp")
        srcs: Source files glob pattern
        deps: Additional dependencies
    """
    all_deps = deps or []

    java_binary(
        name = name,
        srcs = srcs,
        main_class = main_class,
        deps = all_deps,
    )

def all_package_tests(name, packages):
    """Creates a test_suite that includes all package tests.

    Args:
        name: Name of the test suite
        packages: List of package names (e.g., ["my-app", "my-cli"])
    """
    native.test_suite(
        name = name,
        tests = ["//packages/{}:tests".format(pkg) for pkg in packages],
    )
