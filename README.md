# Twitter Clone

A Twitter clone built with Django, Postgres, HTMX, Celery, Redis and Docker.
It's development was performed with Cursor as discussed in this [blog post](https://www.mitchell-harle.dev/twitter-clone/).

## Features

- User authentication and profiles
- Tweet creation with text and images
- Like and retweet functionality
- User following system
- Responsive design with Bootstrap 5
- Infinite scrolling feed with HTMX

## Prerequisites

- Python 3.10+
- Poetry
- Docker and Docker Compose

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/twitter-clone.git
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Set up pre-commit hooks:
   ```bash
   # Install the git hooks
   pre-commit install

   # Run pre-commit on all files
   pre-commit run --all-files
   ```

4. Build the development environment for the first time:
   ```bash
   make build
   ```

5. Start the development environment:
   ```bash
   make start
   ```

6. Access the application at `http://localhost:8000`

### Testing
Make sure the development environment is running with `make start`, tests use the postgres DB.

Testing requires Playwright, install with:
```bash
make setup-tests
```

Run unit tests and E2E tests with:
```bash
make test
```

To run Playwright tests in headed mode so you can see them execute run:
```bash
make test-e2e
```

## Code Quality Tools

This project uses several tools to maintain code quality:

- **Ruff**: For linting and code formatting
- **Mypy**: For static type checking
- **Pre-commit**: For running checks before commits
- **Playwright**: For automated E2E testing
