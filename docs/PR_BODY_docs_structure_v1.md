# [FEATURE] Structure documentation v1.0.0 et chemins numérotés

## Objectif

Harmoniser l’arborescence `docs/` : regrouper les livrables **version 1.0.0** dans `docs/v1.0.0/`, appliquer des **préfixes numériques** (`00_`, `01_`, …) aux fichiers transverses à la racine de `docs/`, et mettre à jour toutes les références (README, CHANGELOG, specs, code, tests).

## Périmètre implémenté

- Dossier **`docs/v1.0.0/`** avec :
  - `00_public_api.md` (contrat public stable)
  - `01_checklist_go.md` (checklist GO)
  - `02_release_notes.md`
  - `03_release_beta_rc_recommendation.md`
- Racine **`docs/`** :
  - `02_dev_diary.md` (journal)
  - `03_release_validation_checklist.md`
  - `04_verify_test_mirror.py` (script miroir tests / modules)
- Suppression des anciens noms sans préfixe / hors `v1.0.0/`.
- Mise à jour des liens GitHub et chemins relatifs dans le dépôt.

## Fichiers principaux créés/modifiés

| Action | Chemin |
|--------|--------|
| Créés | `docs/v1.0.0/00_public_api.md`, `01_checklist_go.md`, `02_release_notes.md`, `03_release_beta_rc_recommendation.md` |
| Créés | `docs/02_dev_diary.md`, `docs/03_release_validation_checklist.md`, `docs/04_verify_test_mirror.py` |
| Supprimés | `docs/public_api_1_0_0.md`, `checklist_go_1_0_0.md`, `release_notes_1_0_0.md`, `release_beta_rc_recommendation.md`, `dev_diary.md`, `release_validation_checklist.md`, `verify_test_mirror.py` |
| Modifiés | `README.md`, `CHANGELOG.md`, `docs/00_dev_constraints.md`, `docs/01_specifications.md`, `src/baobab_web_api_caller/__init__.py`, `docs/examples/*.py`, `tests/.../integration_external/*` |

## Choix de conception

- **Un dossier par version semver** (`v1.0.0`) pour les artefacts de release figés ; les documents transverses restent à la racine de `docs/` avec ordre lexicographique explicite (`00_`, `01_`, puis `02_`–`04_`).
- **Conservation** de `04_verify_test_mirror.py` : le script reste utile (vérifie `gaps 0` pour le miroir tests/modules) ; seul le chemin change.

## Tests ajoutés/mis à jour

- Aucun test applicatif modifié ; références dans `integration_external` mises à jour.

## Résultats des validations

- **black** : OK (`python -m black --check src tests docs/examples`)
- **pylint** : OK — `10.00/10` sur `src/baobab_web_api_caller`
- **mypy** : OK — `Success: no issues found in 55 source files` (`python -m mypy src`)
- **flake8** : OK (`python -m flake8 src tests`)
- **bandit** : OK (`python -m bandit -r src -q`)
- **pytest** : **162 passed**, **1 skipped** (scénario delay/timeout optionnel) avec `BAOBAB_RUN_EXTERNAL_INTEGRATION=1`
- **coverage** : **93.27 %** (seuil ≥ 90 %)
- **miroir** : `python docs/04_verify_test_mirror.py` → `gaps 0`

## Risques / points d’attention

- **Liens externes** (wikis, issues, sites) pointant vers les anciens chemins `docs/public_api_1_0_0.md` etc. : à mettre à jour manuellement.
- Sous **PowerShell**, utiliser `$env:BAOBAB_RUN_EXTERNAL_INTEGRATION="1"` pour activer l’intégration externe.

## Hors périmètre volontaire

- Modification du comportement runtime de la librairie.
- Publication PyPI / tag Git (actions mainteneur).

---

## Résumé global (synthèse PR)

Réorganisation documentaire pour clarifier **livrables par version** vs **docs transverses**, avec chemins stables et préfixes numériques.

## Matrice de conformité (extraits cahier des charges — `docs/01_specifications.md`)

| Exigence | Statut |
|----------|--------|
| Journal structuré (`docs/02_dev_diary.md`) | OK |
| Contrat public documenté (`docs/v1.0.0/00_public_api.md`) | OK |
| Traçabilité CHANGELOG | OK |
| Qualité (black, flake8, pylint, mypy, bandit, pytest, couverture) | OK (voir ci-dessus) |
| Tests intégration externes opt-in | OK avec `BAOBAB_RUN_EXTERNAL_INTEGRATION=1` |

## Risques résiduels éventuels

- Dépendance réseau pour intégration externe ; un test peut rester skipped si services tiers lents ou indisponibles.

## Suggestions de roadmap post-V1

- Client **async** (httpx / aiohttp) en option.
- Support **`Retry-After`** pour backoff.
- CI optionnelle avec job réseau pour `integration_external`.
