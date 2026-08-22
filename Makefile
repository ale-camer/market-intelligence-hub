.PHONY: format lint typecheck test coverage check

format:
	ruff format src/ tests/

lint:
	ruff check src/ tests/ --fix

typecheck:
	mypy src/ tests/

test:
	pytest tests/ -v

coverage:
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

check: format lint typecheck coverage
