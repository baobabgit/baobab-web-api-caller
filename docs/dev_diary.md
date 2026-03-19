# Journal de développement

## 2026-03-19 20:17:50

### Modifications
- Amélioration de `ErrorResponseMapper` : messages d’exceptions HTTP plus lisibles via raison standard quand disponible (`HTTP {status_code} {raison}`), et inclusion de `WWW-Authenticate` parmi les headers diagnostiques (notamment pour le 401).
- Mise à jour des tests de `ErrorResponseMapper` pour valider les messages et l’inclusion de `WWW-Authenticate`.

### Impact
- Les exceptions HTTP levées par le transport et le downloader contiennent désormais un message plus directement interprétable au premier regard, tout en conservant le filtrage de headers et l’extrait de body tronqué.

## 2026-03-19 20:10:06

### Modifications
- Renforcement minimal et lisible du cycle de vie des ressources HTTP : fermeture “safe” de la `requests.Session` et de la `requests.Response` uniquement lorsque les objets sont initialisés.
- Ajout d’un test unitaire dans le downloader validant que la réponse streaming est bien fermée en cas d’erreur d’écriture disque (`OSError`), en plus des cas déjà couverts (`requests` / erreurs HTTP).

### Buts
- Éviter toute fuite de ressources en cas d’exception non liée directement à `requests`, tout en gardant le code simple et testable.

### Impact
- Garantie renforcée de fermeture effective des ressources dans des scénarios d’erreur supplémentaires, sans changement de l’API publique ni du comportement fonctionnel.

## 2026-03-17 21:54:57

### Modifications
- Audit complet de l’arborescence `src/baobab_web_api_caller` et `tests/baobab_web_api_caller` pour vérifier la granularité miroir des tests (un fichier de test par classe, arborescence alignée, classes abstraites testées via implémentations concrètes).
- Validation que tous les composants prioritaires (transport, pagination, core, exceptions, auth) disposent déjà de fichiers de test dédiés et respectent les conventions (`Test...`, arborescence miroir, doubles concrets pour les abstractions).

### Buts
- Confirmer la conformité de la suite de tests aux contraintes de développement sans introduire de refactoring inutile.

### Impact
- Aucune modification de code ou de tests n’a été nécessaire ; la couverture globale (>= 90 %) et la structure miroir des tests sont déjà conformes aux contraintes du projet.

## 2026-03-17 21:45:41

### Modifications
- Ajustement des métadonnées de packaging (`pyproject.toml`) pour passer en statut de maturité "Alpha" (Development Status :: 3 - Alpha).
- Mise à jour du `README.md` pour distinguer l'installation utilisateur (`pip install baobab-web-api-caller`) de l'installation en mode développement (`pip install -e ".[dev]"`), et clarifier la section de validation locale (qualité).

### Buts
- Préparer une première release V1 crédible en reflétant un niveau de maturité réaliste et une expérience d’installation/validation explicite.

### Impact
- Les consommateurs disposent d’indications claires pour installer et valider la librairie, et les métadonnées de distribution reflètent mieux l’état actuel du projet.

## 2026-03-17 21:41:45

### Modifications
- Alignement de la documentation externe (`README.md`) avec les capacités actuelles de pagination et de query params (clarification de ce qui reste hors V1).
- Mise à jour de `docs/01_specifications.md` pour préciser que le mapping d’erreurs expose un contexte HTTP utile (code, extrait de body, métadonnées) et que la pagination prend en compte les query params multi-valués.

### Buts
- Resynchroniser la documentation avec l’état réel du code sans introduire de nouvelles promesses fonctionnelles.

### Impact
- Les lecteurs disposent d’une description fidèle des capacités de transport, de mapping d’erreurs et de pagination, cohérente avec l’implémentation actuelle.

## 2026-03-17 19:23:50

### Modifications
- Évolution de `BaobabRequest` pour accepter des query params typés `Mapping[str, str | Sequence[str]]`, avec gel et validation des valeurs uniques ou séquentielles.
- Mise à jour de `RequestUrlBuilder` pour encoder correctement les clés répétées (via `urlencode` avec `doseq=True`) et conserver toutes les valeurs.
- Adaptation de `Paginator._parse_query_params` pour reconstruire des valeurs uniques ou listées à partir de `next_page_url`, préservant les paramètres dupliqués entre les pages.
- Mise à jour de `ApiKeyQueryAuthenticationStrategy` pour ajouter l’API key sans écraser les valeurs existantes (conversion en séquence si nécessaire).
- Ajout/ajustement des tests unitaires (`RequestUrlBuilder`, `Paginator`, `ApiKeyQueryAuthenticationStrategy`) pour couvrir clés simples, clés répétées, mélange de clés et pagination avec paramètres dupliqués.

### Buts
- Supporter proprement les cas de query string avec clés répétées tout en conservant la simplicité de l’API publique et la compatibilité V1.

### Impact
- Les appels HTTP peuvent désormais transporter des paramètres multi-valués de manière explicite et stable, y compris via l’authentification par query param et la pagination, sans régression sur les usages existants.

## 2026-03-17 19:02:00

### Modifications
- Enrichissement de `HttpException` et des exceptions HTTP dérivées (client/serveur/auth) avec des attributs `status_code`, `body_excerpt` et un sous-ensemble d'en-têtes utiles.
- Mise à jour de `ErrorResponseMapper` pour construire ces exceptions enrichies à partir de `BaobabResponse` (401, 404, 429, autres 4xx, 5xx).
- Ajustement du transport (`HttpTransportCaller`) pour utiliser les nouvelles signatures d'exceptions de retry (429, 5xx).
- Ajustement/extension des tests unitaires (`ErrorResponseMapper`, exceptions HTTP, transport) pour couvrir les cas 401/404/429/autres 4xx/5xx, body vide/long, headers filtrés.
- Mise à jour de `README.md` et du `CHANGELOG.md` pour documenter le mapping d'erreurs enrichi.

### Buts
- Rendre les exceptions HTTP projet plus parlantes pour le diagnostic (logs, observabilité) sans alourdir l'API publique ni exposer l'intégralité des payloads.

### Impact
- Les consommateurs continuent de capturer les mêmes types d'exceptions, mais disposent désormais d'un message structuré et d'attributs supplémentaires pour inspecter le contexte HTTP en erreur.

## 2026-03-17 18:50:44

### Modifications
- Fermeture explicite de la `requests.Session` dans `HttpTransportCaller` (via `finally`) afin d’éviter toute fuite de ressources, y compris en cas de retry/exception.
- Fermeture explicite de chaque `requests.Response` dans `HttpTransportCaller` après décodage (appel à `response.close()`).
- Fermeture explicite de la `requests.Session` et de la `requests.Response` streaming dans `BulkFileDownloader` (fermeture garantie même en cas d’erreur HTTP ou d’exception d’écriture).
- Ajustement des tests unitaires pour vérifier la fermeture effective de la session et des réponses côté transport et downloader.
- Mise à jour du `CHANGELOG.md` (section `Unreleased` / correctifs de cycle de vie des ressources HTTP).

### Buts
- Corriger le cycle de vie des ressources réseau (`requests.Session` / `requests.Response`) pour éviter les fuites de sockets/connexions.

### Impact
- Le transport synchrone et le downloader libèrent désormais systématiquement les ressources HTTP, sans changer l’API publique ni le modèle de composition existant.

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

