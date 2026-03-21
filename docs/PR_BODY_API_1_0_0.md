# [FEATURE] API publique stable 1.0.0 — exports, doc et packaging

## Objectif

Préparer le **freeze du contrat public** pour la version **1.0.0** (Semantic Versioning) : surface
d’API volontaire, documentée et importable depuis le package racine, sans exposition accidentelle.

## Périmètre implémenté

- Extension de `baobab_web_api_caller.__all__` : exceptions, stratégies d’authentification,
  politiques `RetryPolicy` / `RateLimitPolicy`, contrats de pagination (`PageResult`,
  `NextPageUrlExtractor`, `PageExtractor`), `BaobabWebApiCaller`.
- Version **`1.0.0`** dans `__version__` et `pyproject.toml` ; classifier **Production/Stable**.
- Documentation : `docs/public_api_1_0_0.md`, `docs/checklist_go_1_0_0.md`, README (limites, API stable, ce que fait / ne fait pas la lib).
- `CHANGELOG.md` : section **[1.0.0]** avec contenu précédemment [Unreleased] + stabilité API.
- Tests : exports importables, version attendue.
- Journal de développement mis à jour.

## Fichiers principaux créés/modifiés

| Fichier | Rôle |
|---------|------|
| `src/baobab_web_api_caller/__init__.py` | Exports publics + doc contrat stable |
| `pyproject.toml` | `version`, `Development Status` |
| `docs/public_api_1_0_0.md` | Table de référence du contrat 1.x |
| `docs/checklist_go_1_0_0.md` | Checklist GO (état coché partiel ; CI à finaliser) |
| `README.md` | API stable, limites, périmètre fonctionnel |
| `CHANGELOG.md` | Release 1.0.0 |
| `docs/dev_diary.md` | Traçabilité |
| `tests/baobab_web_api_caller/test_public_api_exports.py` | Nouveaux tests |
| `tests/baobab_web_api_caller/test_package_metadata.py` | Version 1.0.0 |

## Choix de conception

- **Un seul point d’entrée documenté** : `__all__` = liste exhaustive des symboles garantis en 1.x.
- **Sous-modules non listés** : peuvent changer sans bump majeur tant qu’ils ne sont pas promus dans `__all__`.
- **Pas de dépendance nouvelle** : uniquement ré-exports et documentation.

## Tests ajoutés/mis à jour

- `test_public_api_exports.py` : import de tous les symboles `__all__`, unicité, ordre alphabétique.
- `test_package_metadata.py` : version `1.0.0`.

## Résultats des validations

*(À remplir sur la CI / machine du relecteur avant merge.)*

- black: `python -m black --check src tests`
- pylint: `python -m pylint src tests`
- mypy: `mypy .`
- flake8: `python -m flake8`
- bandit: `python -m bandit -r src`
- pytest: `python -m pytest`
- coverage: seuil ≥ 90 % (`pyproject.toml`)

## Risques / points d’attention

- **Import initial** : plus de symboles au chargement du package racine ; impact négligeable pour une lib typique.
- **Utilisateurs** qui importaient uniquement depuis des sous-modules : inchangé ; la promotion racine est additive.

## Hors périmètre volontaire

- Tag Git `v1.0.0` et publication PyPI : à faire après validation humaine finale.
- Exécution des tests d’intégration externes sur l’environnement CI : opt-in documenté.

---

## Self-review (relecture PR)

- [x] Cohérence `__all__` / `docs/public_api_1_0_0.md`
- [x] Pas d’import circulaire évident
- [x] Semver et README alignés sur « stable 1.0.0 »
- [ ] Pipeline vert sur le dernier commit *(à confirmer)*

**Verdict** : prêt pour review pair puis merge si CI locale + checklist release OK.
