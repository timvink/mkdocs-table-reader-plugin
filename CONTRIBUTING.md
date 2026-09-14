# Contribution Guidelines

Thanks for considering to contribute to this project! Some guidelines:

- Go through the issue list and if needed create a relevant issue to discuss the change design. On disagreements, maintainer(s) will have the final word.
- You can expect a response from a maintainer within 7 days. If you haven’t heard anything by then, feel free to ping the thread.
- This package tries to be as simple as possible for the user (hide any complexity from the user). Options are only added when there is clear value to the majority of users.
- When issues or pull requests are not going to be resolved or merged, they should be closed as soon as possible. This is kinder than deciding this after a long period. Our issue tracker should reflect work to be done.

## Development setup

This project uses [uv](https://docs.astral.sh/uv/). Install the project and its development dependencies with:

```bash
uv sync
```

## Testing

Run the unit tests and the linter with:

```bash
make test
```

Or separately:

```bash
uv run pytest --cov=mkdocs_table_reader_plugin --cov-report term-missing tests
uv run ruff check src/ tests/
```

If it makes sense, writing tests for your PRs is always appreciated and will help get them merged.

### Code Style

Make sure your code *roughly* follows [PEP-8](https://www.python.org/dev/peps/pep-0008/) and keeps things consistent with the rest of the code. `ruff` is configured in `pyproject.toml` and fixes what it can automatically.

We use google-style docstrings.

## Documentation

Preview the documentation site locally with:

```bash
make serve_docs
```

Every push to `master` deploys the site to GitHub Pages through the `documentation.yml` workflow. You can also deploy by hand with `make deploy_docs`.

## Release

1. Update `__version__` in `src/mkdocs_table_reader_plugin/__init__.py` and add an entry to `CHANGELOG.md`.
2. Commit, then tag and push:

    ```bash
    git tag v<version>
    git push origin master --tags
    ```

3. Create a GitHub release for the tag. That triggers the `pythonpublish.yml` workflow, which runs the tests and publishes to PyPI.
