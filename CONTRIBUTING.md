# Contribution Guidelines

Thanks for considering to contribute to this project! Some guidelines:

- Go through the issue list and if needed create a relevant issue to discuss the change design. On disagreements, maintainer(s) will have the final word.
- You can expect a response from a maintainer within 7 days. If you haven’t heard anything by then, feel free to ping the thread.
- This package tries to be as simple as possible for the user (hide any complexity from the user). Options are only added when there is clear value to the majority of users.
- When issues or pull requests are not going to be resolved or merged, they should be closed as soon as possible. This is kinder than deciding this after a long period. Our issue tracker should reflect work to be done.

## Testing

Make sure to install an editable version before running tests:

```python
pip install -r tests/test_requirements.txt
pip install -e .
pytest --cov=mkdocs_table_reader_plugin --cov-report term-missing tests
```

If it makes sense, writing tests for your PRs is always appreciated and will help get them merged.

In addition, this project uses pyflakes for static code checking:

```python
pip install pyflakes
pyflakes tests/ mkdocs_table_reader_plugin/
```

#### Code Style

Make sure your code *roughly* follows [PEP-8](https://www.python.org/dev/peps/pep-0008/) and keeps things consistent with the rest of the code.

We use google-style docstrings.

## Documentation

They need to be deployed manually:

```bash
mkdocs gh-deploy --force
```

## Release

Update `setup.py`.

```bash
git tag <version>
git push origin <version>
```

Then manually create a github release to trigger publishing to pypi.
