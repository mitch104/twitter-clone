# Twitter Clone

A Twitter clone built with Django, Postgres and HTMX.

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

4. Start the development environment:
   ```bash
   docker-compose up --build
   ```

5. Access the application at `http://localhost:8000`

### Testing

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
