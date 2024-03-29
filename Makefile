.PHONY: install-dev
install-dev:
	python -m pip install --editable .[dev,test]
	pre-commit install

.PHONY: coverage
coverage:
	coverage run -m pytest tests/
	coverage report -m

.PHONY: docker-test
docker-test:
	docker build -t py-tester .
	docker run -it --rm py-tester

.PHONY: build-dist
build-dist:
	python -m pip install --upgrade build
	python -m build

.PHONY: clean
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.mypy_cache' -exec rm -rf {} +
	rm -rf .tox
	rm -f coverage.xml
	rm -f coverage.json
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .coverage.*
	find . -name '.pytest_cache' -exec rm -rf {} +
	rm -rf dist
	rm -rf build
