#!/bin/bash

echo "Setting up Twitter Clone project..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create default static image directory if not exists
mkdir -p twitter_clone/static/img
echo "Created static directories"

# Check if .env file exists, otherwise create it
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "DEBUG=1" > .env
    echo "SECRET_KEY=django-insecure-change-this-in-production" >> .env
    echo "DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]" >> .env
    echo "DATABASE_URL=postgres://postgres:postgres@db:5432/twitter_clone" >> .env
    echo "POSTGRES_PASSWORD=postgres" >> .env
    echo "POSTGRES_USER=postgres" >> .env
    echo "POSTGRES_DB=twitter_clone" >> .env
    echo ".env file created with default values"
fi

# Build and start Docker containers
echo "Building and starting Docker containers..."
docker-compose up -d --build

# Wait for containers to be ready
echo "Waiting for containers to be ready..."
sleep 10

# Run migrations
echo "Running migrations..."
docker-compose exec web python twitter_clone/manage.py makemigrations core
docker-compose exec web python twitter_clone/manage.py migrate

echo "Twitter Clone setup complete!"
echo "You can now access the application at http://localhost:8000/"
echo "Create a superuser with: docker-compose exec web python twitter_clone/manage.py createsuperuser"
