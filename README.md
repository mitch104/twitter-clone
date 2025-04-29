# Twitter Clone

A simple Twitter clone built with Django and PostgreSQL.

## Features

- User registration and authentication
- Post tweets with text and images
- Follow/unfollow other users
- Like/unlike tweets
- Retweet functionality
- Share tweets via URL
- User profiles with bio and profile picture

## Tech Stack

- Django 4.2
- PostgreSQL
- Docker & Docker Compose
- Bootstrap 5
- jQuery

## Setup and Installation

### Prerequisites

- Docker and Docker Compose

### Installation Steps

1. Clone the repository:
   ```
   git clone <repository-url>
   cd twitter-clone
   ```

2. Start the Docker containers:
   ```
   docker-compose up -d --build
   ```

3. Create a superuser:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

4. Visit `http://localhost:8000` in your browser

### Development

- Run migrations:
  ```
  docker-compose exec web python manage.py makemigrations
  docker-compose exec web python manage.py migrate
  ```

- Collect static files:
  ```
  docker-compose exec web python manage.py collectstatic
  ```

- Create a superuser:
  ```
  docker-compose exec web python manage.py createsuperuser
  ```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 