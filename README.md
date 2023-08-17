# Getting started with the project

## Prerequisites

-   Install `pipenv` [https://pipenv.pypa.io/en/latest/](https://pipenv.pypa.io/en/latest/)

## Installation

```bash
$ pipenv install
```

## Start the project

### Docker

```bash
$ docker-compose up
```

### Run locally

```bash
$ pipenv run python main.py
```

## Migrations

### Prerequisites

You will need to install `postgresql@14` on your machine in order to run the migrations.

```bash
$ brew install postgresql@14
```

### Create a migration

```bash
$ pipenv run alembic revision --autogenerate -m "Migration name"
```

### Run migrations

```bash
$ pipenv run alembic upgrade head
```

### Reverse migrations

```bash
$ pipenv run alembic downgrade -1
```

## Scripts

Create Database Schema

```bash
$ sh _scripts/create_db_schema.sh
```

Drop Database Schema

```bash
$ sh _scripts/drop_db_schema.sh
```

Generate requirements.txt

```bash
$ sh _generate_requirements.sh
```

## VS Code setup for formatting

Add the following to your `settings.json`:

```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    },
    "python.formatting.blackArgs": ["--line-length", "120"],
    "files.associations": {
        "*.py": "python"
    },
    "python.analysis.importFormat": "relative"
}
```
