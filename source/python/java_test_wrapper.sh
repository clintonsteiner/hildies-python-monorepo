#!/bin/bash
# Wrapper script for running Java tests with Bazel

set -e

TEST_CLASS=$1
shift
SRCS="$@"

BASEDIR="src/hildie/java/hildie-java-lib"

if [ ! -d "$BASEDIR" ]; then
    echo "Error: Cannot find Java test directory"
    exit 1
fi

cd "$BASEDIR"
mkdir -p bin

# Compile
javac -d bin src/main/java/io/hildie/HildieLibrary.java src/test/java/io/hildie/HildieLibraryTest.java

# Run
java -ea -cp bin "$TEST_CLASS"
