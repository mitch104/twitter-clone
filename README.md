# Twitter Clone

A Twitter clone built with Django, featuring real-time interactions using HTMX.

## Features

- User authentication and profiles
- Tweet creation with text and images
- Like and retweet functionality
- User following system
- Real-time updates using HTMX
- Responsive design with Bootstrap 5

## Prerequisites

- Python 3.11+
- Poetry
- Docker and Docker Compose

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/twitter-clone.git
   cd twitter-clone
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Set up pre-commit hooks:
   ```bash
   # Install pre-commit
   poetry add --group dev pre-commit

   # Install the git hooks
   pre-commit install

   # Run pre-commit on all files
   pre-commit run --all-files
   ```

4. Create a `.env` file in the project root:
   ```env
   DEBUG=1
   SECRET_KEY=your-secret-key
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   POSTGRES_DB=twitter_clone
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   ```

5. Start the development environment:
   ```bash
   docker-compose up --build
   ```

6. Access the application at `http://localhost:8000`

## Code Quality Tools

This project uses several tools to maintain code quality:

- **Ruff**: For linting and code formatting
- **Mypy**: For static type checking
- **Pre-commit**: For running checks before commits

### Pre-commit Hooks

Install pre-commit:
```bash
pre-commit install
```

The following checks are run automatically before each commit:
```bash
pre-commit run --all-files
```
