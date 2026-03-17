# Journal de développement

## 2026-03-17 16:53:52

### Modifications
- Suppression du dossier `scripts/`.
- Ajout des composants `ResponseDecoder`, `JsonResponseDecoder` et `ErrorResponseMapper`.
- Intégration du décodage et du mapping d'erreurs dans le transport HTTP synchrone.
- Ajout/ajustement des tests unitaires (JSON nominal/invalide, 401/404/429/4xx/5xx).

### Buts
- Standardiser le décodage JSON et transformer les erreurs HTTP/décodage en exceptions du projet.

### Impact
- Les couches supérieures peuvent s'appuyer sur un transport qui renvoie des réponses décodées et des erreurs normalisées.

## 2026-03-17 18:17:02

### Modifications
- Enrichissement de `README.md` (principes, architecture, pointeurs vers exemples).
- Ajout d’exemples supplémentaires dans `docs/examples/` (service caller, pagination).
- Nettoyage de l’API publique au niveau package (`baobab_web_api_caller.__init__`).
- Durcissement des tests du downloader (validations + overwrite).
- Mise à jour du `CHANGELOG.md`.

### Buts
- Consolider la documentation, l’API publique et la qualité globale en préparation de la V1.

### Impact
- Documentation et exemples plus complets, et meilleure ergonomie d’import côté utilisateur.

## 2026-03-17 18:04:53

### Modifications
- Ajout du sous-package `download` et du composant `BulkFileDownloader` (streaming par chunks).
- Écriture atomique via fichier `.part` puis renommage pour éviter les fichiers partiels.
- Ajout d’un exemple minimal d’utilisation dans `docs/examples/`.
- Ajout/ajustement des tests unitaires (streaming, erreurs HTTP, timeouts, collision de fichier).

### Buts
- Télécharger des ressources distantes volumineuses sans les charger en mémoire (streaming).

### Impact
- La librairie supporte désormais un cas d’usage “fichier” séparé de la consommation JSON.

## 2026-03-17 17:54:47

### Modifications
- Ajout du sous-package `pagination` (contrats et implémentation génériques).
- Ajout des composants `PageResult`, `PageExtractor`, `NextPageUrlExtractor` et `Paginator`.
- Ajout de tests multi-pages (URLs relatives, URL absolue rejetée si host différent).

### Buts
- Permettre d’itérer simplement sur des ressources paginées dont la page suivante est déterminée par le contenu.

### Impact
- Les couches applicatives peuvent consommer des pages/items en restant découplées du format exact des réponses.

## 2026-03-17 17:26:45

### Modifications
- Intégration effective de `RetryPolicy` et `RateLimitPolicy` dans `HttpTransportCaller`.
- Ajout d’abstractions de temps/attente injectables pour des tests déterministes.
- Ajout de tests couvrant : succès immédiat, succès après retry, échec final, throttling (intervalle minimal).

### Buts
- Rendre le transport plus robuste face aux erreurs temporaires et aux limitations de débit, sans tests instables.

### Impact
- Les appels HTTP peuvent être rejoués de manière contrôlée et respecter un débit minimal configuré.

## 2026-03-17 17:04:47

### Modifications
- Ajout du sous-package `service` et de la façade `BaobabServiceCaller`.
- Ajout des helpers `get`, `post`, `put`, `patch`, `delete`, `head`, `options`.
- Ajout des tests unitaires d’assemblage (fusion headers par défaut/spécifiques, délégation au transport).

### Buts
- Proposer une API de confort pour construire/exécuter des requêtes HTTP à partir d’une configuration centralisée.

### Impact
- Les couches applicatives peuvent appeler un service REST via une façade stable, sans couplage au transport concret.

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

