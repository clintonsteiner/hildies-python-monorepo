# Deploying Documentation to GitHub Pages

The documentation is automatically built and deployed to GitHub Pages when changes are pushed to the `master` branch.

## Setup (One-time)

1. **Enable GitHub Pages in your repository settings:**
   - Go to your repository on GitHub
   - Navigate to Settings → Pages
   - Under "Build and deployment":
     - Source: Select **"GitHub Actions"**
   - Save the settings

2. **Add Hildie's image:**
   - Place `hildie.jpeg` in `docs/source/_static/` directory
   - Commit and push this file

## Workflow

The GitHub Actions workflow (`.github/workflows/docs.yml`) will:

1. Trigger on pushes to `master` that modify files in `docs/`
2. Install Sphinx and required dependencies
3. Build the HTML documentation
4. Deploy to GitHub Pages

## Manual Deployment

You can also manually trigger the deployment:

1. Go to the "Actions" tab in your GitHub repository
2. Select "Build and Deploy Documentation" workflow
3. Click "Run workflow"

## Viewing the Documentation

Once deployed, your documentation will be available at:
```
https://<username>.github.io/<repository-name>/
```

For this repository:
```
https://clintonsteiner.github.io/python-monorepo/
```

## Local Preview

To preview the documentation locally before pushing:

```bash
cd docs
make html
open build/html/index.html
```

## Troubleshooting

### Build fails on GitHub Actions

Check the Actions logs for errors. Common issues:
- Missing dependencies (add to `docs/requirements.txt`)
- Broken links or references in `.rst` files
- Missing image files

### 404 on GitHub Pages

- Ensure GitHub Pages is set to use "GitHub Actions" as the source
- Check that the workflow completed successfully
- Wait a few minutes for the deployment to propagate

### Styles/images not loading

The `.nojekyll` file in `docs/source/` prevents GitHub Pages from ignoring Sphinx's `_static` directory.
