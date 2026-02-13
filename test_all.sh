#!/bin/bash

# Hildie Multi-Language Test Suite
# Runs all tests across Python, Java, Go, Rust, and Node.js using Python test runner

cd "$(dirname "$0")"
python3 source/python/test_runners.py
