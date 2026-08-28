.PHONY: format lint typecheck test coverage check

format:
	.venv/bin/ruff format src/ tests/

lint:
	.venv/bin/ruff check src/ tests/ --fix

typecheck:
	.venv/bin/mypy src/ tests/

test:
	.venv/bin/pytest tests/ -v

coverage:
	.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

check: format lint typecheck coverage
