# Roadmap post-1.0.0 — baobab-web-api-caller

Document de **cadrage** pour ne pas mélanger, dans une release **1.0.x stable**, des chantiers qui
doivent rester **postérieurs** (patch documentaire, évolutions mineures 1.1.x, ou ruptures 2.0.0).

**Références :** `README.md` (limites), `docs/v1.0.0/00_public_api.md` (contrat `__all__`),
`docs/01_specifications.md`, `CHANGELOG.md`.

---

## 1. Portée explicite de la release **1.0.0**

La **1.0.0** est **close** sur le périmètre suivant :

| Domaine | Ce que **1.0.0** livre et fige |
|--------|--------------------------------|
| **Modèle** | Client HTTP(S) **synchrone** (`requests`), `BaobabRequest` / `BaobabResponse`, façade `BaobabServiceCaller`. |
| **Contrat public** | Surface exportée = `baobab_web_api_caller.__all__` (liste dans `docs/v1.0.0/00_public_api.md`). |
| **Auth** | Stratégies Bearer, Basic, clé header/query, pas d’auth — **sans** OAuth2 / mTLS / signature de requête. |
| **Résilience** | `RetryPolicy` + backoff existants ; `RateLimitPolicy` (throttling client) ; **sans** interprétation automatique de `Retry-After`. |
| **Pagination** | Modèle **URL page suivante** (`Paginator` + extracteurs) — **sans** pagination cursor/offset générique intégrée. |
| **JSON** | Décodage générique selon `Content-Type` — **sans** binding Pydantic/dataclasses intégré. |
| **Qualité** | Tests, couverture ≥ 90 %, intégration externe opt-in (HTTPBin / Postman Echo). |

**Règle semver rappelée :** en **1.x.y**, seuls des **ajouts** rétrocompatibles sur `__all__` et des
corrections sans changement d’API observable sont attendus ; toute **rupture** de symbole public ou de
comportement garanti → **2.0.0**.

---

## 2. Ce qui **n’entre pas** dans 1.0.0 (gel volontaire)

Les éléments ci-dessous sont **hors périmètre 1.0.0** : ils ne doivent **pas** être traités comme des
prérequis à une « 1.0.0 complète ». Ils sont reportés selon les colonnes §3–§5.

| Thème | Raison du report |
|-------|-------------------|
| Client **async** (async/await) | Changement de paradigme ; nouvelle surface API et dépendances ; hors modèle synchrone 1.0.0. |
| **`Retry-After`** automatique | Comportement nouveau sur le chemin retry ; spécification serveur variable ; à concevoir en mineure ou option. |
| **Désérialisation** vers modèles métier (Pydantic, etc.) | Hors promesse JSON générique ; dépendances optionnelles et API additionnelle. |
| **OAuth2** (flows, refresh token) | Nouvelles stratégies et état ; complexité et tests dédiés. |
| **Pagination** « riche » (cursor, page/size, liens RFC 5988 généralisés) | Extensions du modèle actuel ; risque de nouveaux contrats publics. |
| **HTTP/2**, multiplexage, pooling avancé | Optimisations transport non requises pour la promesse 1.0.0. |
| **Retry** « avancé » (jitter, circuit breaker, politiques par statut fin) | Évolution comportementale ; à versionner soigneusement. |
| **Breaking** sur `__all__` ou sémantique documentée | Réservé à **2.0.0**. |

> **Principe :** aucun chantier **non stabilisé** de cette liste ne doit être **forcé** dans une
> publication **1.0.x** ; la stable reste un **socle figé**, pas une accumulation de features expérimentales.

---

## 3. Inventaire d’améliorations (non bloquantes pour la stable)

Améliorations possibles **au-delà** du minimum 1.0.0, classées par nature.

### 3.1 Post-1.0 **patch** (`1.0.x` — docs, DX, robustesse sans nouveau contrat)

| Idée | Description |
|------|-------------|
| Documentation | Précisions README, guides « recipes », liens vers `docs/roadmaps/`. |
| Exemples | Nouveaux snippets sous `docs/examples/` sans changer l’API. |
| Ergonomie dev | Scripts, Makefile, tâches VS Code — sans impact runtime. |
| CI | Jobs optionnels (intégration réseau), matrices Python, artefacts. |
| Corrections | Bugs **sans** changement de comportement intentionnel documenté ; typos, messages d’erreur. |
| Observabilité légère | Logs structurés **opt-in** ou hooks documentés **sans** casser les appels existants (si ajoutés en paramètres optionnels uniquement). |

### 3.2 Compatible **1.1.x** (mineur — ajouts rétrocompatibles)

| Idée | Description |
|------|-------------|
| **`Retry-After`** | Respect optionnel de l’en-tête (délai avant retry) derrière un flag / sous-classe de politique. |
| **Retry affiné** | Jitter, max delay, catégories de statuts — **paramètres optionnels** ou nouvelles classes **en plus** des existantes. |
| **Pagination** | Nouveaux extracteurs / helpers (cursor dans le corps, en-tête `Link`) en **ajout** sans casser `Paginator` actuel. |
| **Auth** | Nouvelles `AuthenticationStrategy` (ex. OAuth2 client credentials) **ajoutées** à l’export. |
| **Interop** | Helpers « decode JSON → type » **optionnels** (callbacks), ou extra `baobab-web-api-caller[pydantic]` sans imposer Pydantic au cœur. |
| **Métadonnées réponse** | Exposer davantage d’en-têtes de façon **additive** sur les exceptions ou `BaobabResponse`. |
| **Tests / qualité** | Nouveaux tests, hausse de couverture, pas de changement d’API publique. |

### 3.3 **2.0.0** — breaking (ruptures assumées)

| Idée | Risque / motivation |
|------|---------------------|
| **API async native** | Nouveau module ou remplacement du modèle d’exécution ; impact imports et `BaobabWebApiCaller`. |
| **Refonte `ServiceConfig` / transport** | Changement de construction, suppression de champs, ordre de fusion des en-têtes **si** documenté comme stable aujourd’hui. |
| **Retrait ou renommage** d’un symbole **`__all__`** | Bump majeur obligatoire (cf. `00_public_api.md`). |
| **Sémantique retry/throttle par défaut** | Si le comportement par défaut change de façon observable pour les appels existants. |
| **Python < 3.11** | Si support élargi ou retiré de façon incompatible avec la politique actuelle `>=3.11`. |
| **Fusion avec une couche async** | Si le package unique impose `async` partout ou casse le chemin synchrone historique. |

---

## 4. Roadmap réaliste (proposition)

Horizons **indicatifs** — à ajuster selon charge et retours utilisateurs.

| Phase | Version cible | Focus |
|-------|----------------|-------|
| **A — Stable actuelle** | **1.0.x** | Corrections, doc, CI ; **aucune** feature majeure non mûre. |
| **B — Confort & résilience** | **1.1.0** | `Retry-After` optionnel ; retry/jitter paramétrables ; 1–2 stratégies d’auth supplémentaires si besoin clair. |
| **C — Intégration données** | **1.2.x** (ou 1.1.y) | Helpers pagination additionnels ; hooks / extra optionnel Pydantic **sans** casser le noyau. |
| **D — Grande évolution** | **2.0.0** | Client async **et/ou** refonte majeure du transport ; uniquement après ADR et période de design. |

**Critère de passage 1.0 → 1.1 :** besoin métier récurrent + design validé + tests + pas de régression sur
la suite actuelle.

**Critère de passage vers 2.0 :** rupture **volontaire** et **documentée** ; guide de migration.

---

## 5. Synthèse « quoi où »

| Besoin | Où le mettre |
|--------|----------------|
| Fix typo, bug sans changement d’API | **1.0.x** |
| Nouvelle option / nouvelle classe **en plus** | **1.1.x** |
| Changer un défaut ou retirer un export public | **2.0.0** |

---

## 6. Maintenance de ce document

- Mettre à jour ce fichier lorsqu’une **décision d’architecture** exclut ou inclut un chantier majeur.
- Lier depuis `README.md` (section limites / évolutions) ou `CHANGELOG.md` si une ligne directrice change.

**Dernière révision :** alignement sur la release **1.0.0** stable et séparation explicite patch / 1.1 / 2.0.
