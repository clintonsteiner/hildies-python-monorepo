#!/bin/bash
# Wrapper script for running Rust tests with Bazel

set -e

PACKAGE=$1

cd "source/hildie/rust"

# Run Rust tests for specific package or all
if [ -z "$PACKAGE" ]; then
    cargo test --all
else
    cargo test -p "$PACKAGE"
fi
