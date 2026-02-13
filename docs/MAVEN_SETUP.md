# Maven Central Publishing Setup

Quick setup guide for publishing Java packages to Maven Central.

## Prerequisites

1. **Sonatype Account**: https://central.sonatype.com/account
2. **Registered Namespace**: `io.hildie` at https://central.sonatype.com/account/namespaces
3. **GitHub Secrets** configured

## Step 1: Get Sonatype Credentials

### Option A: Create API Token (Recommended)

1. Go to: https://central.sonatype.com/account/user/settings
2. Click "Create a new token"
3. Fill in:
   - Token name: `github-actions-java-publish`
   - Description: `For GitHub Actions CI/CD`
4. Copy the token (you'll only see it once)

### Option B: Use Username and Password

1. Your Sonatype username (email or username)
2. Your Sonatype password

## Step 2: Add GitHub Secrets

### Via GitHub Web UI:

1. Go to your repository Settings
2. Click "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add first secret:
   - Name: `MAVEN_PUBLISH_USER`
   - Value: Your Sonatype username or email
5. Click "Add secret"
6. Add second secret:
   - Name: `MAVEN_PUBLISH_PASSWORD`
   - Value: Your API token or password
7. Click "Add secret"

### Via GitHub CLI:

```bash
# Set username
gh secret set MAVEN_PUBLISH_USER --body "your-sonatype-username"

# Set password/token
gh secret set MAVEN_PUBLISH_PASSWORD --body "your-sonatype-api-token"

# Verify
gh secret list
```

## Step 3: Verify Setup

The GitHub Actions workflow will automatically:
1. Read `MAVEN_PUBLISH_USER` and `MAVEN_PUBLISH_PASSWORD` secrets
2. Create Maven settings with credentials
3. Run `mvn deploy` when you create a release tag
4. Publish JAR to Maven Central

## Publishing a Release

```bash
# Create release tag
git tag v0.1.0

# Push to GitHub (triggers GitHub Actions)
git push origin v0.1.0

# Wait for GitHub Actions to complete
# Check Actions tab in GitHub to see build progress
```

## Verify Published Package

### Check Maven Central:
- https://central.sonatype.com/artifact/io.hildie/hildie-java-lib
- Search for `io.hildie` in https://central.sonatype.com/search

### Check Maven Repository:
- https://repo1.maven.org/maven2/io/hildie/hildie-java-lib/

### Use in Java Project:

Add to `pom.xml`:
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

## Troubleshooting

### "401 Unauthorized"

**Problem**: Wrong credentials
**Solution**:
1. Verify secrets are correct at GitHub Settings → Secrets
2. Check Sonatype username/password at https://central.sonatype.com/account
3. If using API token, ensure it hasn't expired
4. Re-create token if needed

### "Repository Not Found"

**Problem**: Namespace not registered
**Solution**:
1. Go to https://central.sonatype.com/account/namespaces
2. Click "Create namespace"
3. Enter `io.hildie`
4. Follow verification steps

### "Deployment Failed"

**Problem**: Package already exists
**Solution**:
1. Maven Central doesn't allow re-publishing same version
2. Create new version in `pom.xml`
3. Git tag with new version
4. Push to trigger publish again

Example:
```bash
# If v0.1.0 failed, try v0.1.1
git tag v0.1.1
git push origin v0.1.1
```

### Check GitHub Actions Logs

1. Go to your GitHub repository
2. Click "Actions" tab
3. Find the workflow run for your tag
4. Click on "Publish to Maven Central" step
5. View detailed logs

## Files Updated for Java Publishing

- ✅ `src/hildie/java/hildie-java-lib/pom.xml` - Maven configuration
- ✅ `.github/workflows/bazel.yml` - GitHub Actions workflow
- ✅ `PUBLISHING_GUIDE.md` - Publishing documentation

## Next Steps

1. ✅ Register `io.hildie` namespace
2. ✅ Get Sonatype credentials
3. ✅ Add GitHub secrets (`MAVEN_PUBLISH_USER`, `MAVEN_PUBLISH_PASSWORD`)
4. ✅ Create release tag
5. ✅ GitHub Actions publishes automatically

## References

- [Sonatype Central Portal](https://central.sonatype.com/)
- [Maven Central Publishing](https://central.sonatype.org/publish/publish-manual/)
- [Sonatype Account Settings](https://central.sonatype.com/account/user/settings)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
