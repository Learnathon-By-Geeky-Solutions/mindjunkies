# Getting Started

Follow these steps to set up the project locally:

## Prerequisites

- Python 3.11+
- uv (Python dependency manager)
- PostgreSQL / SQLite
- Docker & Docker Compose (Redis, Elasticsearch)

## Local Development Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies
    cd mindjunkies
    ```
2. Install dependencies:
    ```sh
    pip install uv
    uv sync
    ```
3. Start development:
    ```sh
    cp .env.example .env # Modify the environment variables
    docker compose -f docker-compose.elasticsearch_redis.yml up -d # Start Redis and Elasticsearch

    uv run python manage.py migrate # Run migrations
    uv run python manage.py createsuperuser # Create a superuser
    uv run python manage.py runserver # Start the Django server
    uv run python manage.py tailwind watch # Start Tailwind CSS

    #  You can use make commands as well
    make migrate # Run migrations
    make createsuperuser # Create a superuser
    make tailwind # Start Tailwind CSS
    make runserver # Start the Django server
    ```

4. Open [http://localhost:8000](http://localhost:8000) in your browser.

## Using Docker

```bash
# Build and start containers
docker-compose up --build
```

**For advanced usage go to [advanced-usage.md](advanced-usage.md)**