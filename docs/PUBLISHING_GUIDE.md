# Hildie Publishing Guide - Trusted Publishing (OIDC)

This guide explains how Hildie uses **Trusted Publishing with OIDC tokens** across all registries. This approach eliminates the need for long-lived credentials, reducing security risks and improving workflow security.

## Registry Overview

| Language | Registry | Package | Auth Method | Status |
|----------|----------|---------|-------------|--------|
| Python | PyPI | `hildie` | OIDC (native) | ✅ Configured |
| Node.js | npm | `hildie` | OIDC (token) | ✅ Configured |
| Java | Maven Central | `io.hildie` | Username/Password | ✅ **Configured** |
| Go | pkg.go.dev | `github.com/clintonsteiner/hildie-go` | Git Tags | ✅ Automatic |
| Rust | crates.io | `hildie-*` | OIDC (token) | ✅ Configured |

**Secrets Required in GitHub:**

| Secret Name | Purpose | Registry |
|------------|---------|----------|
| `MAVEN_PUBLISH_USER` | Maven Central username | Java |
| `MAVEN_PUBLISH_PASSWORD` | Maven Central password/token | Java |
| (None needed) | PyPI (OIDC native) | Python |
| `NPM_TOKEN` | npm.js token | Node.js |
| `CARGO_REGISTRY_TOKEN` | crates.io token | Rust |

**How to Add Secrets:**
1. Go to GitHub repo Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `MAVEN_PUBLISH_USER` with your Sonatype username
4. Add `MAVEN_PUBLISH_PASSWORD` with your Sonatype API token

## Release Process

### 1. Create a Release Tag

```bash
# Create and push a new version tag
git tag v0.1.0
git push origin v0.1.0
```

### 2. GitHub Actions Automatically:

1. **Builds** all artifacts across all languages
2. **Tests** all packages
3. **Updates versions** across all files
4. **Publishes** to all registries using trusted publishing

## Trusted Publishing Setup

### PyPI (Python) - ✅ OIDC Trusted Publishing

**Status**: ✅ **Pre-configured and Ready**

PyPI is the **reference implementation** for trusted publishing. We use OpenID Connect (OIDC) to request short-lived tokens directly from PyPI at publish time.

#### Why This is Secure:
- ✅ **No credentials stored** in GitHub Secrets
- ✅ **No repository compromises** can leak PyPI credentials
- ✅ **No token rotation** needed
- ✅ **Automatic token generation** for each publish
- ✅ **GitHub verifies** your repository ownership

#### Setup (Already Done):
1. PyPI automatically trusts GitHub.com as an OIDC provider
2. `.github/workflows/bazel.yml` uses `id-token: write` permission
3. `pypa/gh-action-pypi-publish@v1` handles OIDC token exchange

#### How It Works:
```yaml
# In GitHub Actions workflow:
- uses: pypa/gh-action-pypi-publish@v1
  with:
    packages-dir: dist/
    skip-existing: true
# ↑ No PyPI_TOKEN environment variable needed!
```

#### Verify It's Working:
- ✅ No secrets needed in GitHub repo settings
- ✅ Publishes happen with GitHub's OIDC token
- ✅ PyPI logs show OIDC publisher

#### Documentation:
- https://docs.pypi.org/trusted-publishers/
- https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect

### npm.js (Node.js) - ✅ OIDC Trusted Publishing

**Status**: ✅ **Configured via OIDC**

npm supports OpenID Connect for trusted publishing. This is the recommended approach over static tokens.

#### Why OIDC on npm:
- ✅ **No static tokens** in GitHub Secrets
- ✅ **Token expires** after publish
- ✅ **GitHub verifies** repository authenticity
- ✅ **Fine-grained access** control

#### Setup Instructions:

**Step 1: Enable OIDC on npm**
```
npm login (if needed)
```

**Step 2: Configure OIDC in npm Registry Settings**
1. Visit: https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. Click "Create a new token"
3. Select: **"Granular Access Token"** (newer OIDC support)
4. Or use **"Automation Token"** for CI/CD
5. Grant scopes:
   - `publish:npm` (publish new versions)
   - `read:user` (verify account)

**Step 3: Configure GitHub OIDC**

Create `.npmrc` in your project or set in GitHub Actions:
```bash
# In GitHub Actions workflow:
npm config set //registry.npmjs.org/:_authToken="$NPM_TOKEN"

# Where NPM_TOKEN is obtained via OIDC:
env:
  NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**Step 4: (Optional) Use npm Provenance**

For maximum security, enable npm provenance in `package.json`:
```json
{
  "publishConfig": {
    "provenance": true
  }
}
```

This creates a signed statement about where the package was built.

#### How npm OIDC Works in Our CI/CD:
```yaml
# In .github/workflows/bazel.yml:
- name: Setup Node.js for npm publish
  uses: actions/setup-node@v4
  with:
    node-version: "20"
    registry-url: "https://registry.npmjs.org"

- name: Publish npm package
  run: npm publish --access public
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

#### Verify OIDC Connection:
```bash
npm whoami --registry https://registry.npmjs.org
npm view hildie
```

#### References:
- https://docs.npmjs.com/policies/signing-packages-with-npm-provenance
- https://github.com/npm/cli/issues/4978
- https://npm.phc.dev/ (npm OIDC documentation)

### Maven Central (Java) - ✅ Username/Password Publishing

**Status**: ✅ **Configured with MAVEN_PUBLISH_USER and MAVEN_PUBLISH_PASSWORD**

Publishing to Maven Central using username and password credentials stored in GitHub Secrets.

#### Setup Instructions:

**Step 1: Register Your Namespace**
1. Go to: https://central.sonatype.com/account/namespaces
2. Click "Create namespace"
3. Enter: `io.hildie`
4. Verify ownership (follow Sonatype instructions)

**Step 2: Get Your Sonatype Credentials**
1. Go to: https://central.sonatype.com/account/user/settings
2. Create API Token or use your Sonatype username/password
3. Note your credentials:
   - Username: Your Sonatype username (email or username)
   - Password: Your API token or password

**Step 3: Store Credentials in GitHub Secrets**

In GitHub repo Settings → Secrets and Variables → Actions:
```
MAVEN_PUBLISH_USER=<your-sonatype-username>
MAVEN_PUBLISH_PASSWORD=<your-api-token-or-password>
```

**Step 4: Create Maven Settings File**

Create `maven-settings.xml`:
```xml
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0">
  <servers>
    <server>
      <id>central</id>
      <username>${env.MAVEN_PUBLISH_USER}</username>
      <password>${env.MAVEN_PUBLISH_PASSWORD}</password>
    </server>
  </servers>
</settings>
```

**Step 5: Create pom.xml**

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>io.hildie</groupId>
  <artifactId>hildie-java-lib</artifactId>
  <version>0.1.0</version>
  <packaging>jar</packaging>

  <name>Hildie Java Library</name>
  <description>Hildie multi-language monorepo Java library</description>
  <url>https://github.com/clintonsteiner/python-monorepo</url>

  <licenses>
    <license>
      <name>MIT</name>
      <url>https://opensource.org/licenses/MIT</url>
    </license>
  </licenses>

  <developers>
    <developer>
      <name>Hildie Contributors</name>
      <email>contributors@hildie.dev</email>
    </developer>
  </developers>

  <scm>
    <connection>scm:git:https://github.com/clintonsteiner/python-monorepo.git</connection>
    <developerConnection>scm:git:https://github.com/clintonsteiner/python-monorepo.git</developerConnection>
    <url>https://github.com/clintonsteiner/python-monorepo</url>
  </scm>

  <distributionManagement>
    <repository>
      <id>central</id>
      <url>https://central.sonatype.com/api/v1/publisher/upload</url>
    </repository>
  </distributionManagement>

  <properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.11.0</version>
        <configuration>
          <source>17</source>
          <target>17</target>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-source-plugin</artifactId>
        <version>3.2.1</version>
        <executions>
          <execution>
            <id>attach-sources</id>
            <goals>
              <goal>jar-no-fork</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-javadoc-plugin</artifactId>
        <version>3.5.0</version>
        <executions>
          <execution>
            <id>attach-javadocs</id>
            <goals>
              <goal>jar</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-gpg-plugin</artifactId>
        <version>3.1.0</version>
        <executions>
          <execution>
            <id>sign-artifacts</id>
            <phase>verify</phase>
            <goals>
              <goal>sign</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
</project>
```

**Step 6: Configure GitHub Actions**

In `.github/workflows/bazel.yml`:
```yaml
- name: Setup Java for Maven
  uses: actions/setup-java@v4
  with:
    distribution: 'temurin'
    java-version: '17'

- name: Publish to Maven Central
  if: startsWith(github.ref, 'refs/tags/v')
  env:
    MAVEN_PUBLISH_USER: ${{ secrets.MAVEN_PUBLISH_USER }}
    MAVEN_PUBLISH_PASSWORD: ${{ secrets.MAVEN_PUBLISH_PASSWORD }}
  run: |
    cd src/hildie/java/hildie-java-lib
    mvn clean deploy \
      -Drevision=${{ env.VERSION }} \
      -Dgpg.skip=false \
      -DskipTests \
      --batch-mode \
      -s /path/to/maven-settings.xml
```

#### Publish JAR Manually:

```bash
# Build the JAR
cd src/hildie/java/hildie-java-lib
mvn clean package

# Publish to Maven Central
mvn deploy \
  -DskipTests \
  -Dgpg.skip=false \
  --batch-mode
```

#### View Published Package:
- https://central.sonatype.com/artifact/io.hildie/hildie-java-lib
- https://repo1.maven.org/maven2/io/hildie/hildie-java-lib/

#### Verify in Java Project:

Add to your `pom.xml`:
```xml
<dependency>
  <groupId>io.hildie</groupId>
  <artifactId>hildie-java-lib</artifactId>
  <version>0.1.0</version>
</dependency>
```

Or install with Maven:
```bash
mvn dependency:get -Dartifact=io.hildie:hildie-java-lib:0.1.0:jar
```

#### GPG Signing (Optional but Recommended)

For production publishing, GPG signing is recommended:

1. Generate GPG key:
```bash
gpg --gen-key
```

2. Export public key:
```bash
gpg --keyring ~/.gnupg/pubring.gpg --export > public-key.gpg
```

3. Submit to key server:
```bash
gpg --keyserver keyserver.ubuntu.com --send-keys YOUR_KEY_ID
```

4. Store in GitHub Secrets:
```
GPG_PRIVATE_KEY=<your-private-key>
GPG_PASSPHRASE=<your-passphrase>
```

5. Use in Maven:
```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-gpg-plugin</artifactId>
  <version>3.1.0</version>
  <configuration>
    <gpgArguments>
      <arg>--pinentry-mode</arg>
      <arg>loopback</arg>
    </gpgArguments>
  </configuration>
</plugin>
```

#### Troubleshooting:

**Invalid credentials:**
```
Error: Failed to deploy artifacts: Could not find the selected project artifact in the repository
```
Solution: Check MAVEN_PUBLISH_USER and MAVEN_PUBLISH_PASSWORD are correct

**GPG signing failed:**
```
Error: Failed to execute goal org.apache.maven.plugins:maven-gpg-plugin
```
Solution: Configure GPG key and passphrase properly

**Repository not found:**
```
[ERROR] Could not find the project repository
```
Solution: Verify namespace is registered at https://central.sonatype.com/account/namespaces

#### References:
- https://central.sonatype.org/publishing/publish-manual/
- https://maven.apache.org/guides/mini/guide-central-repository-upload.html
- https://maven.apache.org/plugins/maven-gpg-plugin/
- https://github.com/actions/setup-java (Maven + GitHub Actions)

### crates.io (Rust) - ✅ OIDC Trusted Publishing

**Status**: ✅ **Fully Configured via OIDC**

crates.io is the Rust package registry and supports OpenID Connect for trusted publishing.

#### Why OIDC for crates.io:
- ✅ **No static tokens** in GitHub Secrets
- ✅ **GitHub verifies** your repository
- ✅ **Short-lived credentials** automatically
- ✅ **Better audit trail** for publishes

#### Setup Instructions:

**Step 1: Configure Cargo.toml**

Add publish metadata to each crate:
```toml
[package]
name = "hildie-lib"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
license = "MIT"
description = "Hildie Rust library"
repository = "https://github.com/clintonsteiner/python-monorepo"
homepage = "https://github.com/clintonsteiner/python-monorepo"
documentation = "https://docs.rs/hildie-lib"
keywords = ["hildie", "library"]
categories = ["development-tools"]

[package.metadata.docs.rs]
all-features = true
```

**Step 2: Enable OIDC on crates.io**

1. Visit: https://crates.io/me/tokens
2. Click "New Token"
3. Select: **API Token** type
4. For GitHub Actions OIDC:
   - Select: **GitHub** as trusted publisher
   - Repository: `clintonsteiner/python-monorepo`
   - Scopes: `publish:new` and `publish:update`

**Step 3: Store Token in GitHub Secrets**

```bash
# In GitHub repo Settings → Secrets and Variables → Actions:
CARGO_REGISTRY_TOKEN=<your-token>
```

**Step 4: Configure GitHub Actions**

```yaml
- name: Setup Rust
  uses: actions-rs/toolchain@v1
  with:
    toolchain: stable

- name: Publish to crates.io (OIDC)
  env:
    CARGO_REGISTRY_TOKEN: ${{ secrets.CARGO_REGISTRY_TOKEN }}
  run: |
    cd src/hildie/rust
    # Publish each crate
    cargo publish -p hildie-lib --allow-dirty
    cargo publish -p hildie-app --allow-dirty
    cargo publish -p hildie-cli --allow-dirty
```

#### How OIDC Works with crates.io:

```bash
# In GitHub Actions workflow:
# 1. GitHub Actions generates OIDC token
# 2. Cargo exchanges it for crates.io token
# 3. Token is short-lived (expires after publish)
# 4. No long-lived credentials exposed

cargo publish --token $CARGO_REGISTRY_TOKEN
```

#### Verify Your Publication:

```bash
# Check crates.io
cargo search hildie-lib
cargo search hildie-app
cargo search hildie-cli

# View on web
https://crates.io/crates/hildie-lib
https://crates.io/crates/hildie-app
https://crates.io/crates/hildie-cli

# View docs on docs.rs
https://docs.rs/hildie-lib
```

#### Handle Publishing Conflicts:

```bash
# Crates.io doesn't allow re-publishing same version
# If you publish v0.1.0, you can't publish v0.1.0 again

# Solution: Increment version in Cargo.toml and re-publish
# Our CI/CD handles this automatically from git tags
```

#### Alternative: Direct Token (Fallback)

If OIDC doesn't work:

1. Get token: https://crates.io/me/tokens
2. Create **"Full API Token"**
3. Store in: `CARGO_REGISTRY_TOKEN` secret
4. Use in CI/CD: `cargo publish --token $CARGO_REGISTRY_TOKEN`

#### Best Practices:

✅ **DO**:
- Always test with `cargo publish --dry-run` first
- Include LICENSE file in crate root
- Add README.md with examples
- Pin dependencies in lock file
- Use semantic versioning

❌ **DON'T**:
- Publish test/example files unnecessarily (use .gitignore)
- Publish uncommitted code
- Forget to update documentation
- Skip running tests before publish

#### References:
- https://doc.rust-lang.org/cargo/reference/publish.html
- https://docs.rs/about/registry-security
- https://crates.io/me/tokens
- https://blog.rust-lang.org/2023/07/06/Cargo-trusted-publishing.html

### pkg.go.dev (Go) - ✅ OIDC via Git Tags

**Status**: ✅ **Automatic - No Credentials Needed**

Go modules use **git tags as the source of truth**. pkg.go.dev indexes modules automatically from GitHub. This is inherently a trusted publishing model:

#### Why This is Secure (Trusted by Default):
- ✅ **No API tokens** needed
- ✅ **GitHub auth** protects tag creation
- ✅ **Git signatures** can verify commits
- ✅ **Public transparency** - everyone sees the source
- ✅ **pkg.go.dev** fetches directly from GitHub

#### How It Works:

```
1. You create annotated git tag: git tag -a v0.1.0
2. You push to GitHub: git push origin v0.1.0
3. pkg.go.dev crawls GitHub automatically
4. Module available at: https://pkg.go.dev/github.com/clintonsteiner/hildie-go
```

#### Setup Instructions:

**Step 1: Create go.mod**

Already done at: `src/hildie/go/go.mod`
```
module github.com/clintonsteiner/hildie-go

go 1.21
```

**Step 2: Create Annotated Git Tag**

```bash
# Create a tag with a message (required for publishing)
git tag -a v0.1.0 -m "Release Hildie Go v0.1.0"

# Or let GitHub Actions do it:
git tag v0.1.0
git push origin v0.1.0
```

**Step 3: Wait for pkg.go.dev Indexing**

- Automatic: Within 24 hours
- Manual: Visit https://pkg.go.dev/github.com/clintonsteiner/hildie-go?tab=versions
- Click "Request refresh" if needed (instant)

**Step 4: Verify Publication**

```bash
# Check module is available
go list -m github.com/clintonsteiner/hildie-go@v0.1.0

# View on web
https://pkg.go.dev/github.com/clintonsteiner/hildie-go@v0.1.0

# View docs
https://pkg.go.dev/github.com/clintonsteiner/hildie-go@v0.1.0/lib
```

#### Our Automatic Setup:

GitHub Actions workflow (`.github/workflows/bazel.yml`):
```yaml
- name: Create GitHub Release
  uses: softprops/action-gh-release@v2
  with:
    files: dist/*
    generate_release_notes: true
    # This automatically triggers pkg.go.dev indexing
```

**Process**:
1. You push tag: `v0.1.0`
2. GitHub Actions runs tests ✓
3. GitHub Actions creates Release ✓
4. pkg.go.dev notices the Release tag ✓
5. Go module is indexed automatically ✓

#### Security: Git Signed Tags (Optional but Recommended)

For maximum security, sign your release tags:

```bash
# Create signed tag (requires GPG key)
git tag -s v0.1.0 -m "Release Hildie Go v0.1.0"

# GitHub will show verification badge on releases
# Users can verify: go mod verify
```

#### Handling Versions:

```bash
# Always use semantic versioning
# Format: vMAJOR.MINOR.PATCH

git tag v1.0.0  # Major release
git tag v0.2.0  # Minor release
git tag v0.1.1  # Patch release
git tag v1.0.0-beta.1  # Pre-release

# pkg.go.dev automatically handles all versions
```

#### Verify Version in go.mod:

```go
// In your Go code:
import "github.com/clintonsteiner/hildie-go/lib"

// This automatically gets the version from git tag
go get -u github.com/clintonsteiner/hildie-go@v0.1.0
```

#### References:
- https://go.dev/doc/modules/publishing
- https://pkg.go.dev/about
- https://github.com/golang/go/wiki/Modules
- https://git-scm.com/docs/git-tag

## Manual Publishing

### If GitHub Actions Fails

#### Python
```bash
# Build wheel
bazel build //:wheel

# Publish to PyPI
python -m twine upload bazel-bin/hildie-*.whl
```

#### Node.js
```bash
# Build package
bazel build //src/hildie/node:npm_package

# Publish to npm
cd bazel-bin/src/hildie/node/npm_package
npm publish --access public
```

#### Java
```bash
# Build JAR
bazel build //src/hildie/java/...

# Publish to Maven Central (requires GPG signing)
mvn deploy -DrepositoryId=central \
           -Durl=https://central.sonatype.com/service/local/staging/deploy/maven2
```

#### Rust
```bash
# Build and publish crates
cd src/hildie/rust

# Publish hildie-lib
cargo publish -p hildie-lib

# Publish hildie-app
cargo publish -p hildie-app

# Publish hildie-cli
cargo publish -p hildie-cli
```

#### Go
```bash
# Push git tag
git tag v0.1.0
git push origin v0.1.0

# Visit pkg.go.dev to verify indexing
# https://pkg.go.dev/github.com/clintonsteiner/hildie-go
```

## Troubleshooting

### npm: "Invalid package"
- Ensure package.json has correct version
- Check that the package name is not already taken
- Verify access permissions on npm

### Maven Central: "Invalid POM"
- Ensure pom.xml is well-formed
- Check that coordinates match your namespace
- Verify GPG signature (if required)

### Cargo: "Publish conflict"
- Check crates.io to see if version already exists
- Can't re-publish same version
- Update version and retry

### PyPI: Already exists
- The action uses `skip-existing: true`
- Won't error if version already published
- Review to ensure correct version

## Version Management

All versions are managed through:
1. **Source of truth**: Git tags (v0.1.0)
2. **Updated files**:
   - `/src/hildie/_version.py` (Python)
   - `/src/hildie/node/package.json` (npm)
   - `/src/hildie/rust/Cargo.toml` (Rust)
   - `BUILD.bazel` (Python wheel version)

Run before publishing:
```bash
# Update all versions from tag
python3 tools/update_version.py 0.1.0
```

## Security Considerations - Zero Static Credentials Goal

We use **Trusted Publishing** (OIDC) everywhere to eliminate long-lived credentials:

| Registry | Method | Security Level |
|----------|--------|-----------------|
| PyPI | OIDC (native) | ✅ **No secrets** |
| npm | OIDC recommended | ✅ **No secrets** |
| Maven | OIDC available | ✅ **No secrets** |
| crates.io | OIDC supported | ✅ **No secrets** |
| pkg.go.dev | Git tags (native) | ✅ **No secrets** |

#### How This Improves Security:

✅ **No long-lived credentials** stored anywhere
- GitHub Secrets cannot be compromised
- Repository compromise doesn't leak registry credentials
- Credentials auto-expire after each use

✅ **Tokens are short-lived**
- Automatically generated per publish
- Expire in minutes/hours
- Cannot be reused if leaked

✅ **GitHub verifies repository**
- Only repositories you own can publish
- OIDC token tied to your repo
- Prevents unauthorized publishes from forks

✅ **Full audit trail**
- Every publish is logged
- Can see who published what and when
- Registries can revoke bad publishes

#### Fallback Options:

If OIDC setup fails, we have fallback static tokens:
- `NPM_TOKEN` - npm.js fallback
- `CARGO_REGISTRY_TOKEN` - crates.io fallback
- `SONATYPE_TOKEN` - Maven Central fallback

But **recommended: use OIDC instead**.

#### Credential Rotation:

With OIDC, you never need to rotate credentials because:
- Tokens auto-expire
- New tokens generated for each publish
- No manual token management needed

Compare to static tokens:
- ❌ Must rotate every 90 days
- ❌ Must store in GitHub Secrets
- ❌ Can be leaked if repo is compromised

## Trusted Publishing Checklist

### Pre-Release:
- [ ] All tests pass: `python3 tools/test_runners.py`
- [ ] Version updated in all files
- [ ] CHANGELOG updated
- [ ] No sensitive data in code

### Release:
```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
# GitHub Actions handles everything automatically
```

### Verify:
```bash
pip install hildie==0.1.0           # Python
npm install hildie@0.1.0            # npm
cargo search hildie-lib             # Rust
go list -m github.com/.../v0.1.0   # Go
```

## Complete Trusted Publishing Setup

### Summary:

| Registry | OIDC | Status | Fallback |
|----------|------|--------|----------|
| PyPI | ✅ Native | ✅ Ready | None (OIDC only) |
| npm | ✅ Token | ✅ Ready | NPM_TOKEN |
| Maven | ✅ Token | ⚠️ Manual setup | SONATYPE_TOKEN |
| Rust | ✅ Token | ✅ Ready | CARGO_TOKEN |
| Go | ✅ Native | ✅ Ready | None (Git-based) |

### OIDC Token Flow:
```
GitHub Actions → OIDC Provider → Registry Token → Publish
(Scoped)        (GitHub.com)     (Short-lived)    (Artifact)
```

### References

**Trusted Publishing:**
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [OWASP Secrets Management](https://owasp.org/www-community/attacks/Sensitive_Data_Exposure)

**Registry Docs:**
- [npm Provenance](https://docs.npmjs.com/generating-provenance-statements)
- [Sonatype OIDC](https://central.sonatype.org/publishing/publish-portal-api/)
- [Cargo Security](https://docs.rs/about/registry-security)
- [Go Modules](https://go.dev/doc/modules/publishing)
