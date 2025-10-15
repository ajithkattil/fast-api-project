# Recipes API

A FastAPI-based api for managing recipes.


## Features

- FastAPI for high-performance API
- Pydantic for data validation
- Pytest for Comprehensive testing
- Poetry for dependency management
- Code formatting and linting with Ruff
- Type checking with MyPy

## Getting Started

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:
```bash
git clone <repository-url>
cd recipes-api-service
poetry install
```

4. Create a `.env` file with your configuration:

```bash
# API Configuration
PROJECT_NAME=Recipes API Service
VERSION=0.1.0

# Logging
LOG_LEVEL=INFO
ENABLE_FILE_LOGGING=true

BASE_URL=http://localhost:8000

DATABASE_USER=recipes_api_service_primary
DATABASE_PASSWORD=example
DATABASE_URL=127.0.0.1
DATABASE_PORT=5432
DATABASE_NAME=recipes-api-service
```

3. Activate the virtual environment:
```bash

poetry env use python3.12
poetry env activate
```

5. Configure Poetry and install dependencies
```bash
poetry config http-basic.freshrealm {YOUR_GEMFURY_TOKEN} ""
poetry install
```
6. Start Docker DB container & run migrations
```bash
docker-compose up -d
poetry run alembic upgrade head
```

7. Run the application:
```bash
# Make sure you're in the project root directory
poetry run uvicorn src.main:app --reload
```

The API will be available at http://localhost:8000

## Development

### Code Quality Tools

The project uses several tools to maintain code quality:

- **Ruff**: Code formatting and linting
- **MyPy**: Static type checking

These tools are automatically run on each commit. You can also run them manually:

Setup the project hooks
```bash
pip install pre-commit # brew install pre-commit
pre-commit install
```

Manual checks
```bash
# Run all pre-commit hooks manually
# All
poetry run pre-commit

# Individually
poetry run ruff check .  # Linting
poetry run ruff format .  # Formatting
# Running the mypy rules separately can sometimes produce a different result than with pre-commit
poetry run mypy . 
```

### Running Tests

```bash
poetry run pytest
```
# Test environment secrets
