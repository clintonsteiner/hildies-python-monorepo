# GitHub Actions Workflow - Bazel Build System

Updated GitHub Actions workflow to use Bazel for building everything.

## Changes Made

### Previous Workflow Structure
- ❌ `test` job (matrix testing)
- ❌ `build-java` job (separate Java builds)
- ❌ `build-go` job (separate Go builds)
- ❌ `build-rust` job (separate Rust builds)
- ❌ `build-npm` job (separate npm builds)
- ❌ `publish` job (uses separate tools for each language)

### New Workflow Structure
- ✅ `test` job (Bazel: `bazel test //...`)
- ✅ `build` job (Bazel: `bazel build //source/hildie/...`)
- ✅ `publish` job (Uses Bazel-built artifacts)

## Key Improvements

### 1. Consolidated Build Jobs
**Before**: 5 separate build jobs (build-java, build-go, build-rust, build-npm)
**After**: 1 unified build job using Bazel

```yaml
# New unified build
- name: Build all artifacts with Bazel
  run: |
    bazel build //source/hildie/...
    bazel build //:wheel
```

### 2. Unified Testing
**Before**: Python test runner script
**After**: Bazel test command

```yaml
# New unified testing
- name: Run all tests with Bazel
  run: bazel test //... --test_output=short
```

### 3. Simplified Artifact Collection
All artifacts collected in one place:

```yaml
- name: Collect all artifacts
  run: |
    mkdir -p dist/{java,go,rust,npm}

    # Python wheel
    cp bazel-bin/hildie-*.whl dist/ || true

    # Java JAR files
    find bazel-bin/source/hildie/java -name "*.jar" -exec cp {} dist/java/ \; || true

    # Go binaries
    cp bazel-bin/source/hildie/go/app/hildie-go-app dist/go/ || true
    cp bazel-bin/source/hildie/go/cli/hildie-go-cli dist/go/ || true

    # Rust binaries
    cp bazel-bin/source/hildie/rust/hildie-app/hildie-app dist/rust/ || true
    cp bazel-bin/source/hildie/rust/hildie-cli/hildie-cli dist/rust/ || true

    # npm package
    cp -r bazel-bin/source/hildie/node/npm_package dist/npm/ || true
```

### 4. Reduced Dependencies
- ❌ Removed separate `build-java`, `build-go`, `build-rust`, `build-npm` jobs
- ❌ Removed separate artifact upload steps
- ❌ Removed separate artifact download in publish job
- ✅ Uses single `build` job for all languages

### 5. Simplified Publish Dependencies
**Before**: `needs: [test, build-java, build-go, build-rust, build-npm]`
**After**: `needs: [test, build]`

## Workflow Stages

### 1. Test Stage (Parallel on Linux/macOS)
```
Push/PR → Test (Linux/macOS)
  - Build Python wheel with Bazel
  - Run all tests with Bazel
```

### 2. Build Stage (Linux only)
```
→ Build (Linux)
  - Build all artifacts with Bazel
  - Collect artifacts (Python, Java, Go, Rust, npm)
  - Upload as single artifact
```

### 3. Publish Stage (On version tags)
```
→ Publish (if tag starts with "v")
  - Set version from tag
  - Build all artifacts with Bazel
  - Collect artifacts
  - Publish to PyPI (Python wheel)
  - Publish to npm (npm package)
  - Publish to Maven Central (Java JAR)
  - Publish to crates.io (Rust crates)
  - Go auto-publishes via git tags
  - Create GitHub Release
```

## Benefits

1. **Faster CI/CD**
   - Reduced job count (5 → 1 build job)
   - Parallel builds within Bazel
   - Better caching across builds

2. **Simpler Maintenance**
   - Single build command for all languages
   - Fewer artifact transfer steps
   - Unified test execution

3. **Better Consistency**
   - All languages use same build system
   - Same caching strategy
   - Same build configuration

4. **Reduced Resource Usage**
   - Fewer concurrent jobs
   - Better artifact reuse
   - Smaller workflow file

## Bazel Commands Used

### Testing
```bash
# Run all tests across all languages
bazel test //... --test_output=short
```

### Building
```bash
# Build all source code
bazel build //source/hildie/...

# Build Python wheel
bazel build //:wheel
```

### Artifact Locations
```
bazel-bin/hildie-*.whl                    # Python wheel
bazel-bin/source/hildie/java/*/*.jar         # Java JARs
bazel-bin/source/hildie/go/app/*             # Go app binary
bazel-bin/source/hildie/go/cli/*             # Go CLI binary
bazel-bin/source/hildie/rust/*/               # Rust binaries
bazel-bin/source/hildie/node/npm_package/    # npm package
```

## Setup Requirements

The workflow still requires language toolchain setup for publishing:

- **Java**: For Maven Central publishing
- **Go**: For crates.io publishing
- **Rust**: For crates.io publishing
- **Node.js**: For npm registry publishing

However, **all building** is now done with Bazel.

## Environment Variables

Same as before:
- `MAVEN_PUBLISH_USER` (secret) - Maven Central username
- `MAVEN_PUBLISH_PASSWORD` (secret) - Maven Central password
- OIDC tokens for npm, cargo (auto-managed by GitHub)

## Testing Locally

To verify the workflow logic locally:

```bash
# Test all languages
bazel test //...

# Build all artifacts
bazel build //source/hildie/...

# Build Python wheel
bazel build //:wheel
```

## Troubleshooting

### Build fails in GitHub Actions

Check:
1. Bazel query works: `bazel query "//..."`
2. Local build succeeds: `bazel build //source/hildie/...`
3. BUILD files are correct (check for glob errors)

### Artifacts not found in publish

Verify artifact paths in `dist/` directory:
```bash
bazel build //...
ls -la bazel-bin/source/hildie/java/
ls -la bazel-bin/source/hildie/go/
ls -la bazel-bin/source/hildie/rust/
ls -la bazel-bin/source/hildie/node/
```

### npm publish fails

Check:
- npm package built: `ls -la bazel-bin/source/hildie/node/npm_package/`
- OIDC token obtained in step
- npm registry URL correct

## Files Changed

- `.github/workflows/bazel.yml` - Updated workflow with Bazel-based builds

## Related Documentation

- [HILDIE_NAMESPACES.md](./HILDIE_NAMESPACES.md) - Monorepo structure
- [TESTING.md](./TESTING.md) - Testing guide
- [BUILD.bazel](./BUILD.bazel) - Root Bazel configuration
- [MODULE.bazel](./MODULE.bazel) - Bazel module configuration

## Next Steps

1. ✅ Update GitHub Actions to use Bazel
2. ✅ Test workflow in GitHub Actions
3. ✅ Monitor build times and caching
4. 📋 Consider Bazel remote caching for faster builds
5. 📋 Document Bazel best practices for contributors

## Status

✅ **IMPLEMENTED** - GitHub Actions workflow updated to use Bazel for all builds
