# Journal de développement

## 2026-03-17 16:45:32

### Modifications
- Ajout du contrat `BaobabWebApiCaller` et du builder `RequestUrlBuilder`.
- Ajout du transport HTTP synchrone basé sur `requests` (factory de session + caller).
- Ajout des tests unitaires avec mocks/doubles (construction d’URL, assemblage headers/auth/timeout, wrapping des erreurs).
- Ajout de la dépendance runtime `requests` dans `pyproject.toml`.

### Buts
- Fournir une exécution HTTP synchrone testable et conforme à l’architecture par composition.

### Impact
- Les features suivantes pourront mapper les erreurs HTTP et enrichir le décodage sans changer le transport.

## 2026-03-17 16:17:57

### Modifications
- Ajout du sous-package `config` (ServiceConfig, RetryPolicy, RateLimitPolicy, DefaultHeaderProvider).
- Ajout des tests unitaires en miroir avec validations (URLs, headers, paramètres de politiques).
- Factorisation de la validation des mappings `str -> str` dans `utils/mapping_utils.py`.

### Buts
- Centraliser la configuration transverse des services distants et préparer l’usage par transport/façade.

### Impact
- Les couches futures pourront composer configuration, auth et politiques sans dépendances réseau.

## 2026-03-17 16:03:06

### Modifications
- Ajout du sous-package `auth` avec l’abstraction `AuthenticationStrategy` et des stratégies composables.
- Implémentations: no-auth, bearer, basic, api-key header et api-key query.
- Ajout des tests unitaires en miroir (headers, query params, cas limites) et validations des paramètres.

### Buts
- Fournir une authentification par composition appliquée aux requêtes, sans dépendre du transport HTTP.

### Impact
- Les couches futures pourront injecter la stratégie d’authentification via configuration et l’appliquer avant l’appel réseau.

## 2026-03-17 15:49:38

### Modifications
- Ajout du sous-package `core` avec les objets centraux `HttpMethod`, `BaobabRequest`, `BaobabResponse`.
- Ajout des tests unitaires en miroir couvrant validations, immutabilité et comportements utiles.

### Buts
- Modéliser les échanges HTTP de manière typée et indépendante du transport.

### Impact
- Les couches futures (transport, service) pourront construire/consommer des requêtes/réponses de façon standardisée.

## 2026-03-17 15:33:18

### Modifications
- Ajout du sous-package `exceptions` et de la hiérarchie d’exceptions du projet.
- Ajout des tests unitaires en miroir validant héritage et instanciation.

### Buts
- Disposer d’une hiérarchie d’erreurs claire et homogène, capturable via une exception racine unique.

### Impact
- Les couches `transport`, `core`, `service` pourront mapper les erreurs techniques/HTTP vers des exceptions projet.

## 2026-03-17 15:07:07

### Modifications
- Initialisation de l’arborescence du projet (`src/`, `tests/`, `docs/`).
- Ajout du packaging moderne via `pyproject.toml`.
- Configuration centralisée des outils qualité (black, pylint, mypy, flake8, bandit, pytest, coverage).
- Mise en place d’une base de tests exécutable et d’une contrainte de couverture minimale.

### Buts
- Mettre en place un socle reproductible conforme aux contraintes de développement.

### Impact
- Le projet est prêt à accueillir les features suivantes avec outillage et conventions établis.

