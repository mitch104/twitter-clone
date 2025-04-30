# Run all tests
test:
	export $$(cat .env.test | xargs) && pytest

# Run only E2E tests in headed mode
test-e2e:
	export $$(cat .env.test | xargs) && pytest tests/test_e2e.py --headed --slowmo 1000
