# baobab-web-api-caller

Librairie Python orientée objet pour simplifier, standardiser et fiabiliser les appels HTTP(S)
vers des API REST.

**Version stable 1.0.0** — licence **MIT**. Voir `CHANGELOG.md` et la **surface publique garantie**
dans `docs/public_api_1_0_0.md` (symboles exportés via `baobab_web_api_caller.__all__`).

## API publique stable (1.0.0)

À partir de la **1.0.0**, les symboles listés dans `__all__` au package racine constituent le **contrat
de compatibilité** pour les versions **1.x.y** (ajouts rétrocompatibles autorisés ; ruptures
nécessitant une version **majeure** 2.0.0). Cela inclut notamment :

- modèles et façade : `BaobabRequest`, `BaobabResponse`, `HttpMethod`, `BaobabServiceCaller`, `BaobabWebApiCaller` ;
- transport : `HttpTransportCaller`, `RequestsSessionFactory` ;
- configuration : `ServiceConfig`, `RetryPolicy`, `RateLimitPolicy` ;
- authentification : `AuthenticationStrategy` et les stratégies fournies (Bearer, Basic, clés API, absence d’auth) ;
- exceptions : `BaobabWebApiCallerException` et la hiérarchie documentée (HTTP, transport, timeout, configuration, etc.) ;
- pagination : `Paginator`, `PageResult`, `NextPageUrlExtractor`, `PageExtractor` ;
- téléchargement : `BulkFileDownloader`.

Les **sous-modules** (`baobab_web_api_caller.transport`, `core`, …) restent importables pour des usages
avancés ; seuls les noms dans `__all__` sont **garantis** pour le suivi semver. Référence :
`docs/public_api_1_0_0.md`. Checklist de publication : `docs/checklist_go_1_0_0.md`.

## Ce que la librairie fait / ne fait pas

**Fait** (périmètre 1.0.0) :

- Appels HTTP(S) **synchrones** via `requests`, avec construction d’URL, query params (y compris multi-valeurs), corps JSON ou formulaire.
- Fusion d’en-têtes (défauts service → requête → authentification), retry configurable, throttling, timeouts.
- Mapping des erreurs HTTP et réseau vers des **exceptions typées** du projet.
- Pagination par **URL de page suivante** et téléchargement **streaming** de fichiers.

**Ne fait pas** (hors périmètre ou non garanti dans l’API stable) :

- Client **asynchrone** (async/await) — évolution envisagée ultérieurement.
- Gestion fine de `Retry-After` ou politiques de retry avancées au-delà de ce qui est exposé aujourd’hui.
- Modules internes non exportés dans `__all__` (décoders, `build_call_context`, etc.) : peuvent évoluer sans bump majeur tant qu’ils ne sont pas promus au package racine.

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

## Installation

```bash
python -m pip install -U pip
python -m pip install baobab-web-api-caller
```

Pour un environnement de développement local :

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

## Démarrage rapide

Imports recommandés depuis le **package racine** (contrat stable) :

```python
from baobab_web_api_caller import (
    BaobabServiceCaller,
    BearerAuthenticationStrategy,
    HttpTransportCaller,
    RequestsSessionFactory,
    ServiceConfig,
)
```

### Appel simple via façade de service

Voir `docs/examples/service_caller_minimal.py`.

### Pagination (next page URL dans le contenu)

Voir `docs/examples/pagination_minimal.py`.

### Téléchargement streaming

Voir `docs/examples/bulk_file_downloader_minimal.py`.

`BulkFileDownloader` utilise la même construction de contexte (`build_call_context`) que le transport
classique et **ferme explicitement** la `requests.Session` et la `responses.Response` en streaming
après l’appel (succès comme erreur), pour éviter les fuites ; les erreurs HTTP sont mappées via
`ErrorResponseMapper`, comme dans `HttpTransportCaller`.

### Transport HTTP synchrone (comportement)
Le transport synchrone (`HttpTransportCaller`) applique :
- le throttling avant chaque tentative ;
- le retry selon `RetryPolicy` (erreurs réseau, `429` et `5xx`) ;
- le mapping des erreurs HTTP via `ErrorResponseMapper` ;
- la fermeture explicite des sessions/réponses `requests` pour éviter les fuites ;
- le décodage JSON via `JsonResponseDecoder` uniquement pour `Content-Type: application/json` ou
  `application/*+json` (sinon pas de décodage automatique du corps).

### En-têtes HTTP (fusion)
La fusion finale des en-têtes est centralisée dans `build_call_context` (transport), dans cet ordre de
priorité croissante pour une même clé :
1. en-têtes par défaut du service (`ServiceConfig.default_headers`) ;
2. en-têtes de la `BaobabRequest` (ils écrasent les valeurs par défaut) ;
3. stratégie d'authentification (appliquée en dernier ; peut définir ou remplacer des clés comme
   `Authorization`).

La façade `BaobabServiceCaller` délègue la requête au transport sans fusionner les défauts elle-même.

### Paramètres de requête (query params)
`BaobabRequest.query_params` et le paramètre `query_params=` des raccourcis `BaobabServiceCaller`
(`get`, `post`, etc.) supportent :
- une valeur `str` pour une clé unique ;
- une `Sequence[str]` pour des clés répétées (ex: `{"tag": ["a", "b"]}`).

Lors de la construction de l'URL, les valeurs séquentielles sont encodées comme des clés répétées (même clé, plusieurs occurrences).

La pagination préserve également ces paramètres dupliqués quand ils sont présents dans l'URL de page suivante.

### Tests (granularité miroir)

Règle générale : pour chaque `src/baobab_web_api_caller/**/<nom>.py` (hors `__init__.py`), le fichier de
tests correspondant est `tests/baobab_web_api_caller/**/test_<nom>.py`, avec une classe `Test<…>` dédiée.

**Cas particuliers documentés** :

- `transport/call_context_builder.py` : le dataclass `CallContext` est couvert par
  `tests/.../transport/test_call_context.py` ; la fonction `build_call_context` par
  `tests/.../transport/test_call_context_builder.py` (classe `TestBuildCallContext`).
- `utils/mapping_utils.py` : pas de classe source ; le miroir est `tests/.../utils/test_mapping_utils.py`
  (classe `TestFreezeStrMapping` pour `freeze_str_mapping`).

**Exemples de fichiers déjà présents** (non exhaustif) :

- `auth/authentication_strategy.py` → `tests/.../auth/test_authentication_strategy.py`
- `core/response_decoder.py` → `tests/.../core/test_response_decoder.py`
- `pagination/page_extractor.py`, `next_page_url_extractor.py`, `page_result.py`, `paginator.py` → un
  `test_*.py` par module dans `tests/.../pagination/`
- `transport/http_transport_caller.py`, `requests_session_factory.py`, `call_context_builder.py`,
  `sleeper.py`, `system_sleeper.py`, `system_time_provider.py`, `throttler.py`, `time_provider.py` → un
  `test_*.py` par module dans `tests/.../transport/`
- Exceptions HTTP : pas de `test_http_exceptions.py` agrégé ; un fichier par classe sous
  `tests/.../exceptions/` (ex. `test_http_exception.py`, `test_client_http_exception.py`, …).

Si l’UI Git n’affiche pas tout le dossier `tests/`, développer l’arborescence ou cloner à jour : les fichiers
ci-dessus font partie du dépôt courant. Un cache pytest local obsolète peut encore mentionner d’anciens chemins
de tests : exécuter `pytest` après suppression de `.pytest_cache` si besoin.

## Validation locale (qualité)

```bash
black .
python -m pylint src tests
mypy .
python -m flake8
python -m bandit -r src
pytest
```

Avant une **release** (tag, PyPI), suivre en plus `docs/release_validation_checklist.md` et vérifier
le miroir des tests avec `python docs/verify_test_mirror.py` (attendu : `gaps 0`).

### Tests d'intégration externes (release gate, HTTPBin + Postman Echo)

Une suite **optionnelle** valide le comportement réel contre des services publics de test (**HTTPBin**,
**Postman Echo**). Elle complète les tests unitaires : **elle ne s'exécute pas par défaut** et ne doit
pas être requise dans une CI stricte sans réseau contrôlé.

**Activation (obligatoire pour lancer ces tests)** :

- Définir `BAOBAB_RUN_EXTERNAL_INTEGRATION=1` (valeur exacte `1`).
- Sous **PowerShell** : `$env:BAOBAB_RUN_EXTERNAL_INTEGRATION = "1"`
- Sous **bash** : `export BAOBAB_RUN_EXTERNAL_INTEGRATION=1`

**Lancer uniquement cette suite** (sans couverture, pour éviter un seuil `fail_under` trompeur si vous
ne lancez que ces tests) :

```bash
pytest tests/baobab_web_api_caller/integration_external -m integration_external \
  -o addopts="--strict-markers --strict-config" --no-cov
```

**Scénario delay / timeout (optionnel, plus fragile)** : définir en plus
`BAOBAB_EXTERNAL_INTEGRATION_TIMEOUT_TEST=1` pour exécuter le test qui attend un timeout sur un
endpoint « delay » public. Sans ce flag, ce test est **ignoré**.

Si le réseau ou les services publics sont indisponibles, les tests sont **skippés** avec un message
explicite (pas d'échec attribué à tort à la librairie). Voir `docs/release_validation_checklist.md`.

## Limites et évolutions possibles (post-1.0.0)

- **Retry avancé** : gestion de `Retry-After` (429) et erreurs 408/502/503/504 configurables.
- **Async** : transport asynchrone (httpx/aiohttp) et streaming async.
- **Pagination enrichie** : cas plus avancés (limites de pages, stratégies de navigation, etc.).

Ces points **ne font pas partie du contrat 1.0.0** ; toute évolution majeure de comportement sera
reflétée par semver et le `CHANGELOG.md`.

