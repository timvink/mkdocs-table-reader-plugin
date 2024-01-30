
setup:
	pip install -r tests/test_requirements.txt
	pip install -e .

test:
	pyflakes tests/ mkdocs_table_reader_plugin/
	pytest --cov=mkdocs_table_reader_plugin --cov-report term-missing tests

deploy_docs:
	mkdocs gh-deploy --force