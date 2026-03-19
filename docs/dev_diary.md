# Journal de développement

## 2026-03-19 23:45:00

### Modifications
- Passe validation release : alignement outillage (`mypy`, `flake8`, `black`, `pylint`, `pytest`, couverture) avec ce qui est documenté pour la publication ; ajout `docs/release_validation_checklist.md` et `docs/verify_test_mirror.py`.
- Correctifs techniques : `ErrorResponseMapper._extract_diagnostic_headers` (`Mapping[str, str]`) ; ignores/types de tests pour ABC et `PageResult` ; `RequestUrlBuilder` sans import inutilisé ; `pyproject.toml` `min-similarity-lines` pour pylint ; suppressions pylint locales (`HttpTransportCaller.call`, `BulkFileDownloader.download`, accès interne dans `test_throttler`).
- `CHANGELOG` [Unreleased] : avertissement pré-release + entrées liées à la checklist ; `README` : renvoi vers la checklist et le script miroir.
- Intégration Git sur `main` : commit unique conforme Conventional Commits (`chore(release): ...`).

### Buts
- Empêcher toute release ou entrée de `CHANGELOG` affichant une conformité non démontrée par les commandes du dépôt.
- Respecter `docs/00_dev_constraints.md` : qualité complète, journal structuré, traçabilité.

### Impact
- Les commandes de la checklist atteignent un état vert sur l’arborescence actuelle ; les claims release doivent rester vérifiables via ces commandes.

## 2026-03-19 23:25:07

### Modifications
- Audit croisé code / tests / README / CHANGELOG / dev_diary / `docs/01_specifications.md` sur : détection JSON (`JsonResponseDecoder`), mapping d’erreurs (`ErrorResponseMapper`), fermeture HTTP (`HttpTransportCaller`, `BulkFileDownloader`), fusion d’en-têtes (`build_call_context`), granularité miroir des tests (0 module source sans `test_<module>.py`), query params multi-valeurs (`BaobabRequest`, façade `BaobabServiceCaller`).
- Ajustements documentaires pour supprimer toute ambiguïté : spécifications §10 enrichies (`JsonResponseDecoder`, `ErrorResponseMapper`, `BulkFileDownloader`), README (transport + téléchargement streaming + typo `CHANGELOG`), entrée `CHANGELOG` [Unreleased] pour tracer l’audit.

### Impact
- Aucun écart résiduel identifié entre implémentation et description pour les points audités ; pas de changement de code métier. Les tests existants restent la référence d’exécution.

## 2026-03-19 23:35:00

### Modifications
- Élargissement des annotations `query_params` sur toutes les méthodes de convenance de `BaobabServiceCaller` pour refléter `BaobabRequest` (`str` ou `Sequence[str]` par clé) ; docstrings de façade mises à jour.
- Tests unitaires complétés (GET simple / séquence, POST mixte, DELETE séquence, HEAD simple) et documentation (`README.md`, `docs/01_specifications.md`).

### Impact
- Pas de changement de comportement à l’exécution (seule la surface typée et la doc) ; même conversion `dict(...)` vers `BaobabRequest`.

## 2026-03-19 23:17:27

### Modifications
- Audit automatisé sur l’arborescence : chaque module `src/baobab_web_api_caller/**/*.py` (hors `__init__.py`) possède bien un `tests/baobab_web_api_caller/**/test_<module>.py` correspondant (0 écart détecté dans le dépôt courant). Les fichiers cités comme manquants dans d’anciens constats (`test_authentication_strategy.py`, `test_response_decoder.py`, pagination, transport, exceptions découpées) sont déjà présents ; `test_http_exceptions.py` est absent.
- Ajustement du `CHANGELOG.md`, du `README.md` et de `docs/01_specifications.md` (§12.2) : formulation factuelle sur la granularité miroir, exceptions (`CallContext` / `build_call_context`, `mapping_utils`), absence de fichier d’exceptions agrégé, et note sur cache pytest / affichage partiel dans l’UI Git.

### Impact
- La documentation ne surdéclare plus un état à « prouver » : elle décrit la convention, les cas particuliers et renvoie à l’arborescence réelle. Aucun changement de code métier ni d’API publique.

## 2026-03-19 23:05:00

### Modifications
- Poursuite de la conformité stricte « une classe source ↔ un fichier de test miroir » : couverture de `utils/mapping_utils.py` via `tests/baobab_web_api_caller/utils/test_mapping_utils.py` (classe `TestFreezeStrMapping`).
- Séparation des tests du dataclass `CallContext` (`test_call_context.py`, `TestCallContext`) des tests de `build_call_context` (`test_call_context_builder.py`, classe renommée `TestBuildCallContext`).
- Mise à jour de l’arborescence cible des tests dans `docs/01_specifications.md` (présence de `utils/`).

### Impact
- Couverture globale maintenue au-dessus de 90 % ; aucun changement d’API publique ; pas de refactor métier.

## 2026-03-19 22:46:31

### Modifications
- Consolidation documentaire du flux d'en-têtes : précision dans `build_call_context` (ordre défaut → requête → authentification) et rappels associés dans `DefaultHeaderProvider`, `CallContext`, `HttpTransportCaller.call` et `docs/01_specifications.md` / `README.md`.
- Ajout de tests d'assemblage dans `test_call_context_builder` (écrasement défaut par la requête, écrasement de l'`Authorization` de la requête par la stratégie Bearer).
- Correction dans une entrée antérieure du journal : la priorité réelle pour une même clé est bien *authentification après requête* (ex. `Authorization`), pas l'inverse.

### Impact
- Responsabilité unique de fusion inchangée côté code (`build_call_context`) ; lisibilité et garanties de priorité mieux explicites et testées.

## 2026-03-19 22:30:12

### Modifications
- Resynchronisation documentaire ciblée sur `HttpTransportCaller` : docstring de `call()` enrichie pour expliciter retry, throttling, mapping d’erreurs et fermeture des ressources `requests`.
- Alignement de `README.md` et `docs/01_specifications.md` sur le comportement réel du transport synchrone.

### Impact
- Documentation cohérente avec l’implémentation actuelle, sans changement fonctionnel.

## 2026-03-19 21:02:08

### Modifications
- Évolution de `JsonResponseDecoder` pour reconnaître les content-types JSON usuels : `application/json` et variantes `application/*+json` (ex: `application/problem+json`, `application/vnd.api+json`), y compris avec paramètres (`charset`).
- Ajout des tests unitaires associés (content-type absent, variantes JSON, body vide, JSON invalide).

### Impact
- Meilleure compatibilité avec les APIs REST réelles qui renvoient des media types JSON standards non limités à `application/json`, sans ajout de dépendance ni changement d’API publique.

## 2026-03-19 20:48:25

### Modifications
- Simplification du flux headers : suppression de la fusion redondante des headers par défaut dans `BaobabServiceCaller`.
- Fusion finale conservée uniquement côté transport, via `build_call_context` et `DefaultHeaderProvider` (priorité pour une même clé : requête > défauts ; puis authentification après la requête, ex. `Authorization`).

### Impact
- Code plus lisible et responsabilité plus claire, sans changement de comportement fonctionnel pour l'usage standard avec les transports fournis.

## 2026-03-19 20:44:07

### Modifications
- Remise en conformité stricte de la granularité miroir des tests : création des fichiers de test dédiés manquants pour `auth`, `core`, `exceptions`, `pagination` et `transport`.
- Découpage du test agrégé `test_http_exceptions.py` en fichiers dédiés par classe (`HttpException`, `ClientHttpException`, `ServerHttpException`, `ResourceNotFoundException`, `RateLimitException`).

### Impact
- Couverture maintenue au-dessus de 90 % et suite de tests validée par `pytest -q`.

## 2026-03-19 20:29:43

### Modifications
- Ajout de tests supplémentaires sur la gestion des `query_params` multi-valués : compatibilité de `ApiKeyQueryAuthenticationStrategy` quand le paramètre existe déjà comme séquence, et pagination préservant simultanément plusieurs clés dupliquées.
- Clarification documentaire (README + spécifications) sur le support `str` vs `Sequence[str]` pour représenter des clés répétées dans la query string.

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

