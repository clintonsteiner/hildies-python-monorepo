# Hildie Multi-Language Namespaces

This monorepo contains the complete Hildie ecosystem across multiple programming languages, all managed under the `hildie` namespace and built with Bazel.

## Structure

```
src/hildie/
├── __init__.py                    # Python namespace marker
├── _version.py                    # Shared version
├── hildie_app/                    # Python app
├── hildie_cli/                    # Python CLI
├── hildie_library/                # Python library
├── hildie_archive_git_forks/      # Python tool
├── java/                          # Java namespace
│   ├── hildie-java-lib/          # Java library
│   ├── hildie-java-app/          # Java application
│   └── hildie-java-cli/          # Java CLI
├── go/                            # Go namespace
│   ├── lib/                       # Go library
│   ├── app/                       # Go application
│   ├── cli/                       # Go CLI
│   └── go.mod                     # Go module definition
├── node/                          # Node.js/npm namespace
│   ├── src/                       # TypeScript source
│   │   ├── lib.ts                # Library
│   │   ├── app.ts                # Application
│   │   ├── cli.ts                # CLI tool
│   │   └── index.ts              # Main export
│   ├── package.json              # npm configuration
│   └── tsconfig.json             # TypeScript configuration
└── rust/                          # Rust namespace
    ├── Cargo.toml                 # Workspace definition
    ├── hildie-lib/                # Rust library
    ├── hildie-app/                # Rust application
    └── hildie-cli/                # Rust CLI
```

## Building

### Build All Targets

```bash
bazel build //...
```

### Build by Language

#### Python
```bash
bazel build //:wheel                    # Python wheel
bazel build //:hildie-cli               # Python CLI
bazel build //:hildie-archive-git-forks # Python archiver tool
```

#### Java
```bash
bazel build //src/hildie/java/...                    # All Java targets
bazel build //src/hildie/java/hildie-java-lib       # Java library
bazel build //src/hildie/java/hildie-java-app:hildie-java-app  # Java app
bazel build //src/hildie/java/hildie-java-cli:hildie-java-cli  # Java CLI
```

#### Go
```bash
bazel build //src/hildie/go/...             # All Go targets
bazel build //src/hildie/go/lib             # Go library
bazel build //src/hildie/go/app:hildie-go-app  # Go app
bazel build //src/hildie/go/cli:hildie-go-cli  # Go CLI
```

#### Rust
```bash
bazel build //src/hildie/rust/...                    # All Rust targets
bazel build //src/hildie/rust/hildie-lib            # Rust library
bazel build //src/hildie/rust/hildie-app:hildie-app # Rust app
bazel build //src/hildie/rust/hildie-cli:hildie-cli # Rust CLI
```

#### Node.js / npm
```bash
bazel build //src/hildie/node:npm_package           # npm package
```

## Testing

### Run All Tests

```bash
bazel test //...
```

### Test by Language

```bash
# Python
bazel test //packages/...

# Java
bazel test //src/hildie/java/...

# Go
bazel test //src/hildie/go/...

# Rust
bazel test //src/hildie/rust/...

# Node.js
npm --prefix src/hildie/node test
```

## Running Artifacts

### Python
```bash
bazel run //:hildie-cli
bazel run //:hildie-archive-git-forks
```

### Java
```bash
bazel run //src/hildie/java/hildie-java-app:hildie-java-app
bazel run //src/hildie/java/hildie-java-cli:hildie-java-cli -- "Your Name"
```

### Go
```bash
bazel run //src/hildie/go/app:hildie-go-app
bazel run //src/hildie/go/cli:hildie-go-cli -- "Your Name"
```

### Rust
```bash
bazel run //src/hildie/rust/hildie-app:hildie-app
bazel run //src/hildie/rust/hildie-cli:hildie-cli -- "Your Name"
```

### Node.js
```bash
# Build and run locally
npm --prefix src/hildie/node run build
npm --prefix src/hildie/node run app
npm --prefix src/hildie/node run cli -- "Your Name"
```

## Publishing

All packages are published automatically via GitHub Actions when a git tag is created. Publishing uses trusted publishing (OIDC tokens) where supported.

### Supported Registries

- **PyPI** (Python): `hildie`
- **npm** (Node.js): `@scope/hildie` or `hildie`
- **Maven Central** (Java): `io.hildie`
- **crates.io** (Rust): `hildie-*`
- **pkg.go.dev** (Go): `github.com/clintonsteiner/hildie-go`

### Release Process

```bash
# 1. Create a git tag
git tag v0.1.0

# 2. Push to trigger CI/CD
git push origin v0.1.0

# 3. GitHub Actions automatically:
#    - Builds all artifacts
#    - Updates versions
#    - Tests everything
#    - Publishes to all registries
#    - Creates GitHub Release
```

### Publishing Configuration

See [PUBLISHING_GUIDE.md](./PUBLISHING_GUIDE.md) for:
- Detailed setup for each registry
- Trusted publishing (OIDC) configuration
- Manual publishing instructions
- Troubleshooting guide

## Version Management

All versions are managed through a single source of truth. When releasing:

1. Update the version in `//:version`
2. Create a git tag `v<version>`
3. GitHub Actions automatically:
   - Updates all version files
   - Builds all artifacts
   - Publishes to appropriate registries
   - Creates a GitHub Release

## Architecture

Each language namespace follows the same structure:
- **lib**: Core library functionality
- **app**: Standalone application
- **cli**: Command-line tool

This ensures consistent patterns across the polyglot monorepo.

## Configuration

- **Bazel configuration**: `.bazelrc`
- **Module dependencies**: `MODULE.bazel`
- **Toolchain versions**:
  - Python: 3.12
  - Java: 17
  - Go: 1.21
  - Rust: 1.75

## Namespace Ownership

All packages are owned and maintained under the Hildie namespace:

| Registry | Namespace | Owner | Link |
|----------|-----------|-------|------|
| PyPI | `hildie` | clintonsteiner | https://pypi.org/project/hildie |
| npm | `hildie` | clintonsteiner | https://www.npmjs.com/package/hildie |
| Maven Central | `io.hildie` | clintonsteiner | https://central.sonatype.com/search?q=io.hildie |
| crates.io | `hildie-*` | clintonsteiner | https://crates.io/crates/hildie-lib |
| pkg.go.dev | `github.com/clintonsteiner/hildie-go` | clintonsteiner | https://pkg.go.dev/github.com/clintonsteiner/hildie-go |

All packages use semantic versioning and are released together to maintain consistency across the polyglot ecosystem.
