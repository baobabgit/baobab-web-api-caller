# Checklist de validation avant release

Utiliser cette liste **immédiatement avant** de publier une version (tag Git, GitHub Release, PyPI)
ou de figer une entrée majeure dans `CHANGELOG.md`.

Pour une **1.0.0** ou release majeure de stabilité d’API, compléter aussi `docs/checklist_go_1_0_0.md`
(contrat public, checklist GO).

## Préalables

- [ ] Arbre de travail propre ou changements explicitement listés dans les notes de release.
- [ ] Version dans `pyproject.toml` / `__version__` alignée avec la release prévue (Semantic Versioning).
- [ ] Aucune entrée **nouvelle** dans `CHANGELOG.md` qui ne soit pas vérifiable dans le dépôt
  (fichiers, tests, comportement documenté).

## Contrôles automatisés (depuis la racine du dépôt)

Exécuter dans l’ordre ; tout échec est **bloquant** sauf décision documentée.

| Étape | Commande | Attendu |
|--------|-----------|---------|
| Format | `python -m black --check src tests` | succès |
| Lint (style) | `python -m flake8` | succès |
| Lint (qualité) | `python -m pylint src tests` | succès (code de sortie `0`) |
| Typage | `python -m mypy .` | `Success: no issues found` |
| Sécurité basique | `python -m bandit -r src` | pas de finding bloquant |
| Tests + couverture | `python -m pytest` | tous verts ; couverture ≥ seuil du `pyproject.toml` (`fail_under`) |

Équivalent aux commandes du `README.md` (section « Validation locale »), avec `black --check`
pour une CI stricte.

## Dernier contrôle d’intégration avant publication (opt-in)

**Dernier « GO »** recommandé : exécuter la suite d’**intégration externe** contre **HTTPBin** et
**Postman Echo** (réseau requis). Elle est **hors** du `pytest` par défaut : sans variable
d’environnement, les cas sont **ignorés** (`skip`), pas échoués.

| Étape | Commande | Attendu |
|--------|-----------|---------|
| Intégration externe | `BAOBAB_RUN_EXTERNAL_INTEGRATION=1` puis `pytest tests/baobab_web_api_caller/integration_external -m integration_external -o addopts="--strict-markers --strict-config" --no-cov` | tous verts ou skips explicites (service/réseau) |

- **Optionnel (delay / timeout)** : ajouter `BAOBAB_EXTERNAL_INTEGRATION_TIMEOUT_TEST=1` pour le scénario
  sensible au réseau ; sinon ce test reste ignoré.
- **Documentation** : `README.md` (section tests d’intégration), `docs/01_specifications.md` §12.4.

## Cohérence dépôt / documentation

- [ ] **Miroir tests** : chaque `src/baobab_web_api_caller/**/*.py` hors `__init__.py` a un
  `tests/baobab_web_api_caller/**/test_<module>.py` (exceptions documentées : `CallContext` /
  `build_call_context`, `mapping_utils`). Vérification rapide :

```bash
python docs/verify_test_mirror.py
```

  Attendu : `gaps 0` et code de sortie `0`. En cas d’écart sur des exceptions documentées
  (`test_call_context.py` / `test_call_context_builder.py`, etc.), valider manuellement.

- [ ] **CHANGELOG** : section `[Unreleased]` ou version datée sans affirmation spéculative
  (« conformité », « terminé ») sans point d’ancrage dans le code ou les tests.
- [ ] **README / `docs/01_specifications.md`** : comportements annoncés (JSON, erreurs, headers,
  fermeture HTTP, query multi-valeurs) retrouvés dans `src/` (pas uniquement dans l’historique du journal).

## Après validation

- [ ] Tag Git annoté cohérent avec `CHANGELOG.md` et `pyproject.toml`.
- [ ] Si publication PyPI : artefacts de build (`python -m build`) testés sur environnement propre.

## Historique

- Checklist ajoutée pour verrouiller l’alignement release / qualité / vérité du dépôt (pas de
  « conformité » déclarée sans preuve).
