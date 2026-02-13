#!/bin/bash
# Wrapper script for running Node.js tests with Bazel

set -e

cd "source/hildie/node"

# Install dependencies silently
npm install --silent

# Run tests
npm test
