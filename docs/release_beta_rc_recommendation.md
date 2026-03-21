# Recommandation Beta / RC / stable — passage vers 1.0.0 PyPI

Document de décision pour la **passe de stabilisation** avant publication **PyPI**. À jour lors des
revues release (voir aussi `docs/release_validation_checklist.md`).

## État du dépôt au moment de la dernière validation automatisée

Les contrôles suivants ont été **rejoués avec succès** sur le commit courant :

| Contrôle | Commande | Résultat |
|----------|-----------|----------|
| Format | `python -m black --check src tests docs/examples` | OK |
| Lint style | `python -m flake8` | OK |
| Lint qualité | `python -m pylint src tests` | OK (10/10) |
| Typage | `mypy .` | Success |
| Sécurité | `python -m bandit -r src` | OK |
| Tests + couverture | `python -m pytest` | OK ; ~93 % (seuil ≥ 90 %) |
| Miroir tests | `python docs/verify_test_mirror.py` | `gaps 0` |
| Build packaging | `python -m build` | wheel + sdist OK |
| Intégration externe | `BAOBAB_RUN_EXTERNAL_INTEGRATION=1` + `BAOBAB_EXTERNAL_INTEGRATION_TIMEOUT_TEST=1` + pytest `integration_external` | 12 passed *(réseau requis)* |

> **Note** : sans variable d’environnement, les tests d’intégration sont **skippés** (comportement
> attendu pour CI hors réseau).

## Cohérence version / classifiers

- `pyproject.toml` et `baobab_web_api_caller.__version__` : **1.0.0**
- Classifier PyPI : **Development Status :: 5 - Production/Stable**
- Contrat public : `__all__` + `docs/public_api_1_0_0.md`

Le dépôt est donc **déjà positionné** sur une cible **1.0.0 stable** côté code et métadonnées.

## Choix de publication : `1.0.0b1` vs `1.0.0rc1` vs `1.0.0` direct

| Option | Intérêt | Inconvénient / quand l’éviter |
|--------|---------|-------------------------------|
| **1.0.0b1** | Période beta longue, API encore susceptible d’évoluer. | **Peu adapté** si le contrat `__all__` est déjà figé à 1.0.0 : une bêta devrait refléter une version **0.x** ou un préfixe **1.0.0b*** avec classifier *Beta* et éventuellement une API non finalisée. |
| **1.0.0rc1** | Dernier **gel fonctionnel** avant 1.0.0 final ; utile pour **tester PyPI** et les intégrations sans engager le « premier stable » officiel. | Deux publications à gérer ; à n’utiliser que si vous voulez un **feedback externe** sur l’artefact distribué. |
| **1.0.0 direct** | Simple, aligné avec le dépôt déjà en **1.0.0** + *Stable* ; checklist verte. | Aucun tampon « rc » sur PyPI ; assumez une confiance élevée dans les tests + intégration. |

### Recommandation

1. **Par défaut** : **`1.0.0` direct** sur PyPI **si** :
   - la checklist release est entièrement verte (y compris intégration externe sur une machine avec réseau) ;
   - `CHANGELOG.md` et le tag Git correspondant sont prêts ;
   - aucun chantier bloquant non documenté.

2. **Alternative prudente** : publier **une seule** pré-release **`1.0.0rc1`** (classifier *4 - Beta* ou *RC* selon PyPI), **sans** changer le contrat `__all__`, pour valider les **artefacts** et le **README** sur l’index ; puis **`1.0.0`** final identique au code si aucun retour bloquant.

3. **`1.0.0b1`** : **non recommandé** dans l’état actuel (sauf refonte de la politique de versionnement : alors repasser le code en **0.x** ou **1.0.0b1** avec **API non finalisée** explicitement dans la doc).

## Prochaines actions manuelles

- [ ] Tag Git annoté `v1.0.0` (ou `v1.0.0rc1` si pré-release).
- [ ] Publication PyPI (test ou prod) selon la décision ci-dessus.
- [ ] Vérifier que la page PyPI affiche bien le README et les URLs `project.urls`.
