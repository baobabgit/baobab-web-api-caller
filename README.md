# baobab-web-api-caller

Librairie Python orientée objet pour simplifier, standardiser et fiabiliser les appels HTTP(S)
vers des API REST.

## Principes

- **Orienté objet et composition**: chaque brique (auth, config, transport, pagination, download) est injectable.
- **Une classe par fichier**: structure stable et lisible.
- **Modèles HTTP typés**: `BaobabRequest` / `BaobabResponse` indépendants du transport.
- **Erreurs normalisées**: hiérarchie d’exceptions dédiée au projet, enrichies avec le contexte HTTP utile (code, extrait de body, quelques headers).

## Architecture (aperçu)

- **`config/`**: `ServiceConfig`, `RetryPolicy`, `RateLimitPolicy`, headers par défaut.
- **`auth/`**: stratégies d’authentification (bearer/basic/api key…).
- **`core/`**: modèles et contrats (request/response, decoder, mapper d’erreurs…).
- **`transport/`**: exécution HTTP synchrone via `requests` (retry + throttling).
- **`service/`**: façade de haut niveau (`BaobabServiceCaller`).
- **`pagination/`**: itération générique sur pages via “next page URL”.
- **`download/`**: téléchargement streaming de fichiers (`BulkFileDownloader`).

## Installation (dev)

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Démarrage rapide

### Appel simple via façade de service

Voir `docs/examples/service_caller_minimal.py`.

### Pagination (next page URL dans le contenu)

Voir `docs/examples/pagination_minimal.py`.

### Téléchargement streaming

Voir `docs/examples/bulk_file_downloader_minimal.py`.

## Validation locale

```bash
black .
python -m pylint src tests
mypy .
python -m flake8
python -m bandit -r src
pytest
```

## Améliorations futures (hors V1)

- **Retry avancé**: gestion de `Retry-After` (429) et erreurs 408/502/503/504 configurables.
- **Async**: transport asynchrone (httpx/aiohttp) et streaming async.
- **Pagination enrichie**: support des clés dupliquées en query string (liste), limites de pages, etc.

