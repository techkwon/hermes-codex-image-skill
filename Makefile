PYTHON ?= python3
VENV ?= .venv
ACTIVATE = . $(VENV)/bin/activate

.PHONY: install lint test build smoke clean

install:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && python -m pip install --upgrade pip setuptools wheel
	$(ACTIVATE) && pip install -e .[dev]

lint:
	$(ACTIVATE) && ruff check .

test:
	$(ACTIVATE) && pytest

build:
	$(ACTIVATE) && python -m build

smoke:
	$(ACTIVATE) && hermes-codex-image "Generate a minimal banana icon on a light background" --output /tmp/hermes-codex-image-smoke.png

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache
