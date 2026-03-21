# Checklist GO 1.0.0 — baobab-web-api-caller

Document de suivi pour le gel de l’API et la publication **1.0.0**. Mettre à jour au fil des releases.

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

- [ ] `black --check .` passe *(à exécuter avant tag)*
- [ ] `flake8 src tests` passe
- [ ] `pylint src tests` passe
- [ ] `mypy src` ou `mypy .` passe *(projet : `mypy .`)*
- [ ] `bandit -r src` passe
- [ ] `pytest` passe
- [ ] Couverture >= 90 %
- [ ] Les tests d’intégration externes passent avec activation explicite

## 4. Validation d’intégration externe

- [ ] Les tests HTTPBin passent *(avec `BAOBAB_RUN_EXTERNAL_INTEGRATION=1`)*
- [ ] Les tests Postman Echo passent
- [ ] Scénarios critiques couverts en réel : GET + query, query multi-valeurs, headers, POST JSON, auth, erreur HTTP, timeout/delay si activé
- [x] Les tests externes sont documentés comme opt-in (`README.md`, `docs/release_validation_checklist.md`)
- [x] Les skips réseau sont propres et expliqués (`conftest` intégration)

## 5. Documentation produit

- [x] Le README permet à un développeur de démarrer sans lire le code *(installation, liens exemples, API stable, limites)*
- [x] Le README contient installation, quickstart, auth, erreurs, pagination, download *(sections + exemples)*
- [x] Le README documente explicitement les limites actuelles
- [x] La doc explique ce que la librairie fait et ce qu’elle ne fait pas
- [x] Les exemples sous `docs/examples/` restent valides *(imports sous-modules encore OK ; préférence racine documentée)*
- [x] `CHANGELOG.md` décrit ce qui est visible dans le dépôt pour la 1.0.0
- [x] `docs/dev_diary.md` mis à jour pour cette livraison

## 6. Packaging / publication

- [x] La version dans `pyproject.toml` est passée à `1.0.0`
- [x] Le classifier de maturité est cohérent avec une release stable *(Production/Stable)*
- [x] La description courte et le `README` sont cohérents
- [x] La licence est explicite *(MIT, `pyproject.toml` + README)*
- [x] Le README est prêt pour PyPI *(contenu `readme`)* 
- [ ] Le package s’installe proprement via `pip install` *(valider sur environnement propre avant PyPI)*
- [ ] Un tag Git `v1.0.0` est créé *(après validation finale)*
- [x] Les release notes sont préparées dans `CHANGELOG.md` section `[1.0.0]`

## 7. Décision finale

- [ ] Aucun point bloquant ouvert sur la stabilité API *(revue mainteneur)*
- [ ] Aucun écart connu entre doc et code
- [ ] Aucun chantier critique reporté sans être documenté
- [ ] GO final validé sur le commit exact à publier
