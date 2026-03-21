# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
et ce projet suit le [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

### Added

- **`LICENSE`** : texte **MIT** à la racine ; métadonnées PyPI `license = { file = "LICENSE" }`.
- **`docs/release_notes_1_0_0.md`** : release notes **1.0.0** (résumé installable, liens, pas de promesse hors dépôt).
- **`docs/release_beta_rc_recommendation.md`** : recommandation **Beta / RC / 1.0.0 stable** et trace des
  validations release.

### Changed

- **`pyproject.toml`** : description courte PyPI affinée ; `license` via fichier **LICENSE** ; mots-clés
  et classifiers (**OS Independent**, sujets HTTP / bibliothèques) pour une fiche PyPI complète.
- **`docs/release_validation_checklist.md`** : contrôles **black** (incl. `docs/examples`), **miroir**
  tests, **build** optionnel ; lien vers **`docs/release_beta_rc_recommendation.md`** (Beta / RC /
  stable).
- **README** : réécriture orientée **documentation produit** (PyPI) : proposition de valeur,
  installation, quickstart, authentification, erreurs, pagination, téléchargement, tests d’intégration,
  limites ; liens GitHub pour les chemins `docs/` ; section contributeurs en fin de fichier.
- **`pyproject.toml`** : métadonnées `[project.urls]` (accueil, dépôt, documentation, changelog).

### Fixed

---

## [1.0.0] - 2026-03-21

Première version **stable** : contrat public explicite (`baobab_web_api_caller.__all__`), classifier
PyPI *Production/Stable*, documentation d’API (`docs/public_api_1_0_0.md`) et checklist GO
(`docs/checklist_go_1_0_0.md`).

### Added

- Suite de **tests d’intégration externes** (release gate) sous `tests/baobab_web_api_caller/integration_external/` : HTTPBin + Postman Echo, activation explicite via `BAOBAB_RUN_EXTERNAL_INTEGRATION=1`, marqueur pytest `integration_external`, skip propre si désactivé ou service injoignable ; scénario delay/timeout optionnel via `BAOBAB_EXTERNAL_INTEGRATION_TIMEOUT_TEST=1`.
- `docs/release_validation_checklist.md` : checklist de validation release (qualité + cohérence).
- `docs/verify_test_mirror.py` : script de contrôle rapide fichier de test miroir / module source.
- Alignement typé des raccourcis `BaobabServiceCaller` (`get`, `post`, `put`, `patch`, `delete`, `head`, `options`) sur `BaobabRequest` pour `query_params` : `Mapping[str, str | Sequence[str]] | None`.
- Documentation et tests explicites sur la priorité des en-têtes dans `build_call_context` (défauts < requête < authentification pour une même clé).
- Enrichissement des exceptions HTTP (`HttpException` et dérivées) avec `status_code`, extrait de body texte et sous-ensemble d'en-têtes utiles.
- Support des paramètres de query string sous forme de chaînes ou de séquences de chaînes (`Mapping[str, str | Sequence[str]]`) dans `BaobabRequest`, avec encodage correct des clés répétées dans `RequestUrlBuilder` et support côté pagination.
- Tests supplémentaires + documentation clarifiée pour la gestion des query params multi-valués (séquences, clés répétées) et la compatibilité avec `ApiKeyQueryAuthenticationStrategy`.
- Détection JSON élargie dans `JsonResponseDecoder` pour les content-types JSON usuels (`application/json` et `application/*+json`).
- **Exports publics stables** : le package racine réexporte les exceptions, stratégies d’authentification, `RetryPolicy`, `RateLimitPolicy`, contrats de pagination (`PageResult`, `NextPageUrlExtractor`, `PageExtractor`) et `BaobabWebApiCaller` ; liste figée dans `__all__` (voir `docs/public_api_1_0_0.md`).

### Changed

- **Version et maturité** : `1.0.0`, classifier PyPI `Development Status :: 5 - Production/Stable`.
- Granularité miroir des tests : ajout de `tests/.../utils/test_mapping_utils.py`, de `tests/.../transport/test_call_context.py` pour `CallContext`, et renommage de la classe de tests `TestCallContextBuilder` en `TestBuildCallContext` dans `test_call_context_builder.py` ; arborescence `utils/` documentée dans les spécifications.
- Documentation (README, spécifications) : rappel explicite de la convention de nommage `test_<module>.py` et des exceptions (`CallContext` / `build_call_context`, `mapping_utils`) pour que l’arborescence visible corresponde aux engagements du projet.
- Audit de cohérence documentation / code : précisions sur `JsonResponseDecoder` (règles réelles de `Content-Type`), `ErrorResponseMapper` (messages et en-têtes diagnostiques), `BulkFileDownloader` (fermeture des ressources, `build_call_context`), et typo corrigée dans la liste du `CHANGELOG`.
- Mise en conformité des outils : `mypy` sur `src` et `tests` ; `black` ; `pylint src tests` sans erreur (`pyproject.toml` : `min-similarity-lines` pylint relevé pour limiter les R0801 entre tests ; suppressions locales documentées : complexité `BulkFileDownloader.download`, flux `HttpTransportCaller.call`, accès interne dans `test_throttler`) ; import inutilisé retiré de `RequestUrlBuilder`.
- README : périmètre fonctionnel, limites, lien vers l’API publique stable et checklist GO 1.0.0.

### Fixed

- Fermeture explicite des `requests.Session` après chaque appel dans le transport synchrone.
- Fermeture explicite des `requests.Response` (y compris en streaming) dans le downloader, pour éviter les fuites de ressources.
- Fermeture “safe” des ressources `requests.Session` / `requests.Response` via vérifications d’initialisation, et tests garantissant la fermeture effective en cas d’erreur d’écriture disque.
- Amélioration du diagnostic des exceptions HTTP : messages plus lisibles (raison standard) + extrait de body tronqué + sous-ensemble d'en-têtes (dont `WWW-Authenticate` côté 401).
- Suppression de la fusion redondante des headers par défaut : la fusion finale est effectuée uniquement côté transport (`build_call_context` via `DefaultHeaderProvider`).
- Suite de tests découpée par classe (exceptions HTTP : plus de fichier agrégé `test_http_exceptions.py` dans le dépôt ; un fichier `test_<exception>.py` par classe). Contrôle automatique : `python docs/verify_test_mirror.py` (attendu `gaps 0` ; exceptions de nommage documentées dans le README).
- Typage : `ErrorResponseMapper._extract_diagnostic_headers` accepte un `Mapping[str, str]` (aligné sur `BaobabResponse.headers`).
- Resynchronisation des docstrings/docs sur le transport synchrone (`HttpTransportCaller`) : retry, throttling, mapping d’erreurs et gestion des ressources explicités.

## [0.1.0] - 2026-03-17

### Added

- Bootstrap du projet (packaging moderne, arborescence, outillage qualité, base de tests).
- Hiérarchie d'exceptions du projet.
- Noyau HTTP (HttpMethod, BaobabRequest, BaobabResponse).
- Stratégies d'authentification composables.
- Configuration de service et politiques (retry/throttling).
- Transport HTTP synchrone basé sur `requests`.
- Décodage JSON et mapping d'erreurs HTTP vers les exceptions projet.
- Façade de service `BaobabServiceCaller`.
- Retry et throttling intégrés au transport.
- Pagination générique basée sur une next page URL.
- Téléchargement streaming de fichiers via `BulkFileDownloader`.
