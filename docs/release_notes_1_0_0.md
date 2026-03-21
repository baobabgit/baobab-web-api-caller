# Release notes — baobab-web-api-caller 1.0.0

**Date de référence** : 2026-03-21  
**Type** : première version **stable** (Semantic Versioning).

## Résumé

Première publication **1.0.0** sur PyPI : client HTTP(S) REST **synchrone** basé sur `requests`, avec
façade `BaobabServiceCaller`, configuration (`ServiceConfig`, retry, throttling), authentification
composable, erreurs typées, pagination par URL suivante et téléchargement streaming.

## Installation

```bash
python -m pip install baobab-web-api-caller
```

Python **3.11**, **3.12** ou **3.13**.

## Points clés

- **Contrat public** : symboles garantis listés dans `baobab_web_api_caller.__all__` (voir
  [`docs/public_api_1_0_0.md`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/docs/public_api_1_0_0.md)).
- **Documentation produit** : [`README.md`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/README.md)
  (page PyPI).
- **Qualité** : tests unitaires, couverture élevée, suite d’intégration externe optionnelle (HTTPBin /
  Postman Echo).

## Ruptures de compatibilité

Aucune par rapport aux versions **0.x** publiées précédemment : passage de **0.1.0** (bootstrap) à une
API figée **1.0.0** avec surface exportée explicite.

## Liens

| Ressource | URL |
|-----------|-----|
| Dépôt | https://github.com/baobabgit/baobab-web-api-caller |
| Changelog détaillé | [`CHANGELOG.md`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/CHANGELOG.md) |
| Checklist release | [`docs/release_validation_checklist.md`](https://github.com/baobabgit/baobab-web-api-caller/blob/main/docs/release_validation_checklist.md) |

## Contributeurs

Voir les commits et le journal de développement dans le dépôt.
