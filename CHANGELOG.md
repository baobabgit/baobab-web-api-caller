# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
et ce projet suit le [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

### Added
- Enrichissement des exceptions HTTP (`HttpException` et dérivées) avec `status_code`, extrait de body texte et sous-ensemble d'en-têtes utiles.
 - Support des paramètres de query string sous forme de chaînes ou de séquences de chaînes (`Mapping[str, str | Sequence[str]]`) dans `BaobabRequest`, avec encodage correct des clés répétées dans `RequestUrlBuilder` et support côté pagination.

### Fixed
- Fermeture explicite des `requests.Session` après chaque appel dans le transport synchrone.
- Fermeture explicite des `requests.Response` (y compris en streaming) dans le downloader, pour éviter les fuites de ressources.
- Fermeture “safe” des ressources `requests.Session` / `requests.Response` via vérifications d’initialisation, et tests garantissant la fermeture effective en cas d’erreur d’écriture disque.
- Amélioration du diagnostic des exceptions HTTP : messages plus lisibles (raison standard) + extrait de body tronqué + sous-ensemble d'en-têtes (dont `WWW-Authenticate` côté 401).

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

