# [FEATURE] Stabilisation Beta/RC — checklist release, reco 1.0.0

## Objectif

Rejouer la **checklist de release** sur le commit courant, valider **qualité + intégration externe +
build**, documenter l’absence d’écarts bloquants et **recommander** le passage en **1.0.0b1**,
**1.0.0rc1** ou **1.0.0 direct** pour PyPI.

## Périmètre implémenté

- Rejeu complet des contrôles (voir résultats ci-dessous).
- **`docs/release_beta_rc_recommendation.md`** : synthèse des résultats, tableau de décision
  bêta / RC / stable, **recommandation par défaut : `1.0.0` direct** (alternative **`1.0.0rc1`** si
  besoin d’une pré-release PyPI ; **`1.0.0b1`** non privilégié tant que l’API est déjà figée en 1.0.0).
- **`docs/release_validation_checklist.md`** : black incluant `docs/examples`, ligne miroir tests,
  build optionnel, lien vers la reco Beta/RC.
- **`CHANGELOG.md`** [Unreleased], **`docs/dev_diary.md`**.

## Fichiers principaux créés/modifiés

| Fichier | Rôle |
|---------|------|
| `docs/release_beta_rc_recommendation.md` | **Nouveau** — décision et trace validation |
| `docs/release_validation_checklist.md` | Contrôles complétés + section décision |
| `CHANGELOG.md` | Entrée [Unreleased] |
| `docs/dev_diary.md` | Traçabilité |
| `docs/PR_BODY_BETA_RC_STABILIZATION.md` | Ce corps de PR |

## Choix de conception

- Ne **pas** modifier la version **`1.0.0`** dans le dépôt : elle reflète déjà le gel API ; la reco
  documente plutôt **comment** publier sur PyPI (direct vs `rc1`).
- Intégration externe : succès **conditionné au réseau** ; la checklist rappelle les variables
  d’environnement.

## Tests ajoutés/mis à jour

- Aucun test code modifié ; rejeu manuel de la suite existante.

## Résultats des validations

*(Commit validé lors de la préparation de cette PR.)*

| Outil | Commande | Résultat |
|-------|-----------|----------|
| black | `python -m black --check src tests docs/examples` | OK |
| pylint | `python -m pylint src tests` | 10.00/10 |
| mypy | `mypy .` | Success |
| flake8 | `python -m flake8` | OK |
| bandit | `python -m bandit -r src` | OK |
| pytest | `python -m pytest` | 151 passed, 12 skipped (intégration sans env) |
| coverage | (pytest) | ~93 % (≥ 90 %) |
| verify_test_mirror | `python docs/verify_test_mirror.py` | gaps 0 |
| build | `python -m build` | wheel + sdist OK |
| intégration externe | `BAOBAB_RUN_EXTERNAL_INTEGRATION=1` + `BAOBAB_EXTERNAL_INTEGRATION_TIMEOUT_TEST=1` + pytest `integration_external` | **12 passed** |

## Matrice de conformité (aperçu `docs/01_specifications.md`)

| Thème | Statut |
|-------|--------|
| Qualité / typage / sécurité | Aligné checklist |
| Tests unitaires + couverture | Seuil respecté |
| Miroir tests | gaps 0 |
| Intégration réseau | OK avec opt-in |
| Packaging | Build OK |
| Doc release / semver | `release_beta_rc_recommendation.md` |

## Risques / points d’attention

- **Intégration externe** : dépend de HTTPBin / Postman Echo ; en CI sans réseau, les skips sont
  normaux — rejouer avant PyPI sur poste avec réseau.
- **Publication** : tag `v1.0.0` et PyPI restent **manuelles**.

## Hors périmètre volontaire

- Changement de version vers `1.0.0rc1` dans le dépôt (décision mainteneur après lecture de la reco).
- Publication PyPI effective.

---

## Résumé global

Checklist release **complète et documentée** ; recommandation **1.0.0 direct** ou **1.0.0rc1** prudente ;
aucun écart bloquant détecté sur les contrôles rejoués.

## Roadmap post-V1 (suggestions)

- Async client, retry `Retry-After`, pagination avancée (voir README / CHANGELOG).

---

## Self-review

- [x] Cohérence `CHANGELOG` / `dev_diary` / checklist
- [x] Résultats d’intégration externes reproductibles avec `cmd` + variables d’environnement

**Verdict** : prêt pour merge.
