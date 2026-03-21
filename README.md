# baobab-web-api-caller

**Client HTTP(S) REST synchrone pour Python** — modèles typés (`BaobabRequest` / `BaobabResponse`), façade
`BaobabServiceCaller`, transport `requests` avec retry, throttling et erreurs normalisées.

| | |
|---|---|
| **Version** | 1.0.0 (stable) |
| **Python** | 3.11 à 3.13 |
| **Licence** | MIT |
| **Dépendance runtime** | `requests` ≥ 2.32 |

> **PyPI** : sur la page du projet, les liens vers les fichiers du dépôt pointent vers GitHub. En local,
> les chemins `docs/...` désignent les mêmes fichiers.

---

## Proposition de valeur

- **Appels REST synchrones** sans réinventer la roue : URL, query (simple ou multi-valeurs), JSON ou
  formulaire, timeouts.
- **Authentification composable** : Bearer, Basic, clé en en-tête ou en query, ou pas d’auth.
- **Résilience configurable** : politique de **retry** (tentatives, backoff) et **throttling** (débit).
- **Erreurs exploitables** : exceptions du projet avec `status_code`, extrait de corps et sous-ensemble
  d’en-têtes utiles pour les erreurs HTTP.
- **Pagination** et **téléchargement fichier en streaming** sur la même base (`ServiceConfig` + transport).

Ce que la lib **ne fournit pas** : client **async**, parsing de schémas métier au-delà du JSON générique,
gestion automatique de `Retry-After` (voir [Limites connues](#limites-connues)).

---

## Installation

```bash
python -m pip install -U pip
python -m pip install baobab-web-api-caller
```

Développement du dépôt (outillage qualité) :

```bash
python -m pip install -e ".[dev]"
```

**Contrat public stable** : les symboles garantis en **1.x** sont listés dans `baobab_web_api_caller.__all__`
et décrits dans le dépôt : [`docs/public_api_1_0_0.md`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/docs/public_api_1_0_0.md).

---

## Quickstart

### 1. Construire le service

Imports depuis le **package racine** (recommandé) :

```python
from baobab_web_api_caller import (
    BaobabServiceCaller,
    HttpTransportCaller,
    NoAuthenticationStrategy,
    RequestsSessionFactory,
    ServiceConfig,
)

config = ServiceConfig(
    base_url="https://api.example.com",
    authentication_strategy=NoAuthenticationStrategy(),
    default_timeout_seconds=30.0,
)
transport = HttpTransportCaller.from_service_config(
    service_config=config,
    session_factory=RequestsSessionFactory(),
)
service = BaobabServiceCaller(service_config=config, web_api_caller=transport)
```

### 2. Appeler l’API

La façade expose des raccourcis : `get`, `post`, `put`, `patch`, `delete`, `head`, `options`. Chacun
délègue à `BaobabRequest` + transport (pas de fusion des en-têtes par défaut côté façade : voir
[En-têtes](#en-têtes-et-query-params)).

```python
response = service.get("/v1/status", query_params={"env": "prod"})
assert response.status_code == 200
# JSON décodé si Content-Type: application/json ou application/*+json
data = response.json_data
```

Exemples complets (fichiers exécutables) :

- [Service minimal](https://github.com/baobabgit/baobab-web-api-caller/blob/main/docs/examples/service_caller_minimal.py)

---

## Authentification

Les stratégies implémentent `AuthenticationStrategy` et s’injectent dans `ServiceConfig`.

| Stratégie | Usage typique |
|-----------|----------------|
| `NoAuthenticationStrategy` | Pas d’auth |
| `BearerAuthenticationStrategy` | `Authorization: Bearer <token>` |
| `BasicAuthenticationStrategy` | HTTP Basic (`username` / `password`) |
| `ApiKeyHeaderAuthenticationStrategy` | Clé dans un en-tête (nom + valeur) |
| `ApiKeyQueryAuthenticationStrategy` | Clé dans la query (sans écraser les valeurs existantes) |

```python
from baobab_web_api_caller import BearerAuthenticationStrategy, ServiceConfig

config = ServiceConfig(
    base_url="https://api.example.com",
    authentication_strategy=BearerAuthenticationStrategy(token="votre-jeton"),
)
```

L’ordre de **fusion des en-têtes** pour une même clé est : défauts du service → en-têtes de la requête
→ **authentification en dernier** (peut définir ou remplacer `Authorization`).

---

## En-têtes et query params

- **En-têtes par défaut** : `ServiceConfig.default_headers`.
- **Par requête** : argument `headers=` des raccourcis ou `BaobabRequest.headers`.
- **Query** : `query_params` accepte une `str` par clé ou une `Sequence[str]` pour les clés répétées
  (ex. `{"tag": ["a", "b"]}`), aligné sur `BaobabRequest`.

Le transport synchrone (`HttpTransportCaller`) :

- applique le **throttling** avant chaque tentative ;
- applique le **retry** (`RetryPolicy`) sur erreurs réseau `requests`, statuts **429** et **5xx** ;
- mappe les erreurs HTTP via le mapper interne vers les **exceptions** ci-dessous ;
- ferme les `requests.Session` et `requests.Response` après usage ;
- décode le JSON automatiquement seulement si le `Content-Type` indique du JSON (`application/json` ou
  `application/*+json`).

---

## Erreurs

Les erreurs métier / HTTP exposées publiquement dérivent de `BaobabWebApiCallerException` (voir
[`__all__`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/src/baobab_web_api_caller/__init__.py)).

Principales catégories :

| Exception | Contexte |
|-----------|------------|
| `ConfigurationException` | Configuration ou paramètres invalides |
| `AuthenticationException` | Réponse HTTP **401** |
| `ResourceNotFoundException` | **404** |
| `RateLimitException` | **429** |
| `ClientHttpException` | Autres **4xx** (hors cas ci-dessus) |
| `ServerHttpException` | **5xx** |
| `TimeoutException` | Timeout réseau / requête |
| `TransportException` | Erreur de transport générique |
| `ResponseDecodingException` | Corps JSON attendu mais invalide ou absent |
| `ServiceCallException` | Erreur côté couche service |

Les exceptions HTTP (`HttpException` et sous-classes) exposent notamment `status_code`, un message
lisible, un extrait de corps optionnel et un sous-ensemble d’en-têtes utiles au diagnostic.

```python
from baobab_web_api_caller import ClientHttpException, ResourceNotFoundException

try:
    service.get("/ressource/inconnue")
except ResourceNotFoundException as exc:
    code = exc.status_code  # 404
    _ = str(exc)
```

---

## Pagination

Itération sur les pages via une **URL de page suivante** : implémentez `PageExtractor` (items dans la
réponse) et `NextPageUrlExtractor` (lien suivant), puis `Paginator`.

Exemple : [`docs/examples/pagination_minimal.py`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/docs/examples/pagination_minimal.py)

---

## Téléchargement (streaming)

`BulkFileDownloader` télécharge vers un fichier local en stream, réutilise la même logique de contexte
que le transport et **ferme** la `requests.Session` et la `requests.Response` en fin d’appel (succès ou
erreur). Les erreurs HTTP suivent le même mapping que `HttpTransportCaller`.

Exemple : [`docs/examples/bulk_file_downloader_minimal.py`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/docs/examples/bulk_file_downloader_minimal.py)

---

## Tests d’intégration externes (opt-in)

Suite **optionnelle** contre **HTTPBin** et **Postman Echo** (réseau requis). **Sans activation**, les
tests sont **ignorés** (`skip`), pas des échecs — adapté à une CI sans Internet.

```bash
export BAOBAB_RUN_EXTERNAL_INTEGRATION=1   # bash
# PowerShell : $env:BAOBAB_RUN_EXTERNAL_INTEGRATION = "1"

pytest tests/baobab_web_api_caller/integration_external -m integration_external \
  -o addopts="--strict-markers --strict-config" --no-cov
```

Scénario **delay / timeout** supplémentaire (optionnel, plus sensible au réseau) :
`BAOBAB_EXTERNAL_INTEGRATION_TIMEOUT_TEST=1`.

Détails : [`docs/release_validation_checklist.md`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/docs/release_validation_checklist.md).

---

## Limites connues

- Pas de client **asynchrone** (async/await).
- Retry : pas d’interprétation automatique de **`Retry-After`** pour calibrer les attentes.
- Décodage JSON : selon les règles de `Content-Type` ci-dessus ; pas de désérialisation vers des
  modèles Pydantic/dataclasses intégrée.
- Évolutions envisagées (hors contrat détaillé ici) : retry avancé, async, pagination plus riche — voir
  `CHANGELOG.md`.

---

## Validation locale et release

Contrôle qualité courant (depuis la racine du dépôt) :

```bash
python -m black --check src tests
python -m flake8
python -m pylint src tests
mypy .
python -m bandit -r src
python -m pytest
```

Avant publication : [`docs/release_validation_checklist.md`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/docs/release_validation_checklist.md),
[`CHANGELOG.md`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/CHANGELOG.md).

---

## Pour les contributeurs

- Convention de tests : un fichier `test_<module>.py` par module source sous `src/baobab_web_api_caller/`
  (exceptions documentées : `CallContext` / `build_call_context`, `mapping_utils`). Vérification :
  `python docs/verify_test_mirror.py` (attendu : `gaps 0`).
- Cahier des charges : `docs/01_specifications.md`.
- Journal : `docs/dev_diary.md`.

---

## Licence

MIT — voir le dépôt pour le texte complet.
