"""Test rule macros for Hildie polyglot monorepo."""

load("@rules_shell//shell:sh_test.bzl", "sh_test")

def java_integration_test(name, test_class, srcs, resources = None, **kwargs):
    """Creates a Java integration test using native javac.

    Args:
        name: Test target name
        test_class: Full class path to run (e.g., "io.hildie.HildieLibraryTest")
        srcs: Source files to compile
        resources: Resource files
        **kwargs: Additional arguments
    """
    sh_test(
        name = name,
        srcs = ["//tools:java_test_wrapper.sh"],
        args = [test_class] + srcs,
        data = srcs + (resources or []),
        **kwargs
    )

def go_integration_test(name, srcs, importpath, **kwargs):
    """Creates a Go integration test using native go test.

    Args:
        name: Test target name
        srcs: Source files
        importpath: Import path (e.g., "github.com/clintonsteiner/hildie-go/lib")
        **kwargs: Additional arguments
    """
    sh_test(
        name = name,
        srcs = ["//tools:go_test_wrapper.sh"],
        args = [importpath],
        data = srcs + [
            "//source/hildie/go:lib",
            "//source/hildie/go:app",
            "//source/hildie/go:cli",
        ],
        **kwargs
    )

def rust_integration_test(name, package, **kwargs):
    """Creates a Rust integration test using cargo test.

    Args:
        name: Test target name
        package: Package name to test (e.g., "hildie-lib")
        **kwargs: Additional arguments
    """
    sh_test(
        name = name,
        srcs = ["//tools:rust_test_wrapper.sh"],
        args = [package],
        data = [
            "//source/hildie/rust:hildie-lib",
            "//source/hildie/rust:hildie-app",
            "//source/hildie/rust:hildie-cli",
        ],
        **kwargs
    )

def node_integration_test(name, **kwargs):
    """Creates a Node.js integration test using npm test.

    Args:
        name: Test target name
        **kwargs: Additional arguments
    """
    sh_test(
        name = name,
        srcs = ["//tools:node_test_wrapper.sh"],
        data = [
            "//source/hildie/node:npm_package",
        ],
        **kwargs
    )
