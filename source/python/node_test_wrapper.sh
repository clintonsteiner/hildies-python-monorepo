#!/bin/bash
# Wrapper script for running Node.js tests with Bazel

set -e

cd "src/hildie/node"

# Install dependencies silently
npm install --silent

# Run tests
npm test
