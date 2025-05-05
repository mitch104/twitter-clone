build:
	docker-compose build

start:
	docker-compose up


setup-tests:
	playwright install
	playwright install-deps

# Run all tests
test:
	poetry run pytest

# Run only E2E tests in headed mode
test-e2e:
	poetry run pytest tests/test_e2e.py --headed --slowmo 1000
