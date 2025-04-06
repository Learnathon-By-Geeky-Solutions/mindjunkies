# Getting Started

Follow these steps to set up the project locally:

## Prerequisites
- Python 3.11+
- uv
- PostgreSQL / SQLite

## Setup Instructions
1. Clone the repository:
    ```sh
    git clone https://github.com/Learnathon-By-Geeky-Solutions/mindjunkies
    cd mindjunkies
    ```
2. Install dependencies:
    ```sh
    uv sync
    ```
3. Start development:
    ```sh
    cp .env.example .env # Modify the environment variables
    uv run python manage.py createsuperuser
    uv run python manage.py runserver
    uv run python manage.py tailwind watch
    ```
4. Open [http://localhost:8000](http://localhost:8000) in your browser.
