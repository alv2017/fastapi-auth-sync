.PHONY: help
help:  ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: lint
lint:  ## Linter the code.
	@echo "Linting Code"
	uv run ruff check api tests --fix --show-fixes


.PHONY: format
format:  ## Format the code.
	@echo "Code Formatting"
	uv run ruff format


.PHONY: test
test:  ## Test your code.
	@echo "Run Pytest Tests"
	uv run pytest tests/ -svv --cov=api --cov-report=term-missing:skip-covered --cov-report=xml --cov-fail-under 80
