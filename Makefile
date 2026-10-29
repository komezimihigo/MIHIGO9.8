PYTHON = python
PYTEST = pytest

.PHONY: test lint validate build zip

install:
	python -m pip install -r requirements.txt

check:
	python -m compileall .
	$(PYTEST) -q

lint:
	python -m compileall .
	python -m pytest -q --disable-warnings

validate:
	python scripts/validate_project.py

zip:
	python scripts/build_release.py
