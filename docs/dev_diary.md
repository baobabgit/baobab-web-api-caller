# Journal de développement

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

