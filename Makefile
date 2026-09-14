
setup:
	uv sync

test:
	uv run ruff check src/ tests/
	uv run pytest --cov=mkdocs_table_reader_plugin --cov-report term-missing tests

serve_docs:
	uv run mkdocs serve

deploy_docs:
	uv run mkdocs gh-deploy --force
