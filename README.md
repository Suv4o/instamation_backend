# Getting started with the project

## Prerequisites

-   Install `pipenv` [https://pipenv.pypa.io/en/latest/](https://pipenv.pypa.io/en/latest/)

## Installation

```bash
$ pipenv install
```

## Start the project

```bash
$ pipenv run python main.py
```

## VS Code setup

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
