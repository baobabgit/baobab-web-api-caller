# baobab-web-api-caller

Librairie Python orientée objet pour simplifier, standardiser et fiabiliser les appels HTTP(S)
vers des API REST.

## Installation (dev)

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Validation locale

```bash
black .
python -m pylint src tests
mypy .
python -m flake8
python -m bandit -r src
pytest
```

