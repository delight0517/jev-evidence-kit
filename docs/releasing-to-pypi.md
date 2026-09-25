# PyPI release setup

The repository can publish a wheel and source archive from a GitHub Release using PyPI Trusted Publishing. No long-lived PyPI API token is stored in GitHub.

## One-time account setup

1. Sign in to the owner's PyPI account and open **Publishing**.
2. Add a pending GitHub Actions publisher:
   - PyPI project: `jev-evidence-kit`
   - Owner: `delight0517`
   - Repository: `jev-evidence-kit`
   - Workflow: `pypi-publish.yml`
   - Environment: `pypi`
3. In GitHub repository Settings → Environments, create the `pypi` environment. Add required reviewers if the owner wants a human approval before a release can publish.

A pending publisher does not reserve the package name; another account can register it before the first successful publish. Check the project name again immediately before configuring and releasing.

## Publish a version

1. Update `[project].version` in `pyproject.toml` and keep the matching package/version references consistent.
2. Create a GitHub Release whose tag matches that version (for example, `v0.1.2`).
3. Confirm the `Publish package to PyPI` workflow succeeds, then verify the project page and install command from a clean environment.

Do not report the package as published or installs as customer use until the PyPI project, workflow run, and downstream evidence are read back. Existing v0.1.1 remains the current product release until a new release completes.
