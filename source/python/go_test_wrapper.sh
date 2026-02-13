#!/bin/bash
# Wrapper script for running Go tests with Bazel

set -e

IMPORTPATH=$1

cd "source/hildie/go"

# Run Go tests
go test "$IMPORTPATH"
