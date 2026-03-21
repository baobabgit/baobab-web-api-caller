# Checklist GO 1.0.0 — baobab-web-api-caller

Document de suivi pour le gel de l’API et la publication **1.0.0**.  
**Dernière mise à jour** : alignement sur les passes release, qualité, packaging PyPI et documentation
produit (état coché = validé dans le dépôt courant, sauf actions **manuelles** de publication).

## 1. Stabilité de l’API publique

- [x] Les classes publiques exposées dans `src/baobab_web_api_caller/__init__.py` sont figées pour la 1.0.0 (`__all__` documenté dans `docs/public_api_1_0_0.md`).
- [x] Les signatures publiques de `BaobabServiceCaller` sont figées (contrat typé + docstrings ; évolutions rétrocompatibles en 1.x).
- [x] Les signatures publiques de `BaobabRequest` et `BaobabResponse` sont figées.
- [x] Les stratégies d’authentification publiques sont figées (export racine + liste dans `docs/public_api_1_0_0.md`).
- [x] La hiérarchie d’exceptions publiques est figée (export racine).
- [x] Toute rupture d’API identifiée a été soit supprimée, soit repoussée à une future 2.0.0 (hors `__all__` : modules internes non garantis).

## 2. Comportements fonctionnels couverts

- [x] GET couvert
- [x] POST couvert
- [x] PUT couvert
- [x] PATCH couvert
- [x] DELETE couvert
- [x] HEAD couvert
- [x] OPTIONS couvert
- [x] Headers par défaut + override + auth couverts
- [x] Query params simples couverts
- [x] Query params multi-valeurs couverts
- [x] Retry couvert
- [x] Rate limiting / throttling couvert
- [x] Timeout couvert
- [x] Mapping d’erreurs enrichi couvert
- [x] Pagination couverte
- [x] Download streaming couvert

## 3. Validation qualité

Commandes alignées sur `docs/release_validation_checklist.md` (black inclut `docs/examples`).

- [x] `python -m black --check src tests docs/examples` passe
- [x] `python -m flake8` passe
- [x] `python -m pylint src tests` passe
- [x] `mypy .` passe
- [x] `python -m bandit -r src` passe
- [x] `python -m pytest` passe
- [x] Couverture ≥ seuil du `pyproject.toml` (~93 % au dernier contrôle)
- [x] Les tests d’intégration externes passent avec activation explicite (`BAOBAB_RUN_EXTERNAL_INTEGRATION=1` ; optionnel : `BAOBAB_EXTERNAL_INTEGRATION_TIMEOUT_TEST=1` pour le scénario delay)

## 4. Validation d’intégration externe

- [x] Les tests HTTPBin passent *(avec `BAOBAB_RUN_EXTERNAL_INTEGRATION=1`)*
- [x] Les tests Postman Echo passent
- [x] Scénarios critiques couverts en réel : GET + query, query multi-valeurs, headers, POST JSON, auth, erreur HTTP, timeout/delay si activé
- [x] Les tests externes sont documentés comme opt-in (`README.md`, `docs/release_validation_checklist.md`)
- [x] Les skips réseau sont propres et expliqués (`tests/.../integration_external/conftest.py`)

## 5. Documentation produit

- [x] Le README permet à un développeur de démarrer sans lire le code *(installation, quickstart, liens GitHub)*
- [x] Le README contient installation, quickstart, auth, erreurs, pagination, download
- [x] Le README documente explicitement les limites actuelles
- [x] La doc explique ce que la librairie fait et ce qu’elle ne fait pas
- [x] Les exemples sous `docs/examples/` sont à jour *(imports racine recommandés)*
- [x] `CHANGELOG.md` décrit la version **1.0.0** et l’[Unreleased] reste factuel
- [x] `docs/release_notes_1_0_0.md` : notes de publication synthétiques
- [x] `docs/dev_diary.md` tenu à jour pour les livraisons majeures

## 6. Packaging / publication

- [x] La version dans `pyproject.toml` / `__version__` est **1.0.0**
- [x] Le classifier de maturité est cohérent avec une release stable *(Production/Stable)*
- [x] Description courte PyPI + **README** comme description longue (`readme = "README.md"`)
- [x] Licence explicite : fichier **`LICENSE`** (MIT) + `license = { file = "LICENSE" }` dans `pyproject.toml`
- [x] Mots-clés et classifiers PyPI complétés *(voir `pyproject.toml`)*
- [x] Métadonnées `[project.urls]` présentes *(accueil, dépôt, documentation, changelog)*
- [x] `python -m build` produit wheel + sdist sans erreur ; installation du wheel validée dans un venv propre (`pip install dist/*.whl`, import OK)
- [ ] **Tag Git `v1.0.0`** créé *(action manuelle au moment de la publication)*
- [ ] **Upload PyPI** *(action manuelle : `twine` ou CI)*

## 7. Décision finale

- [x] Aucune incohérence bloquante identifiée entre contrat public (`__all__`), code et doc principale
- [x] Pas d’écart connu documenté entre README / spécifications et comportement `src/` pour les points release
- [x] Chantiers non bloquants (async, Retry-After, etc.) explicitement hors périmètre ou en roadmap *(README / CHANGELOG)*
- [ ] **GO publication PyPI** : à confirmer par le mainteneur au **commit / tag** exact publié *(dernière étape humaine)*

## 8. Références utiles

| Document | Rôle |
|----------|------|
| `docs/release_validation_checklist.md` | Ordre des commandes et contrôles avant tag |
| `docs/release_beta_rc_recommendation.md` | Choix direct 1.0.0 vs pré-release `rc` |
| `docs/public_api_1_0_0.md` | Liste du contrat public stable |
| `docs/release_notes_1_0_0.md` | Texte de GitHub Release / annonce |

## Historique du fichier

- Checklist initiale pour le gel API ; mises à jour successives après intégration externe, doc produit,
  passes Beta/RC, packaging PyPI (**LICENSE**, build, `release_notes_1_0_0.md`).
