# Cahier des charges de développement
## Projet `baobab-web-api-caller`

## 1. Objet du document

Ce document définit le cahier des charges de développement du projet `baobab-web-api-caller`.
Il sert de référence fonctionnelle, technique et organisationnelle pour concevoir, développer,
tester, documenter et maintenir une librairie Python visant à simplifier les appels vers des API
web REST.

Ce cahier des charges intègre les contraintes de développement applicables au projet et les traduit
en exigences concrètes de réalisation.

---

## 2. Présentation du projet

### 2.1 Nom du projet

`baobab-web-api-caller`

### 2.2 Finalité

Le projet a pour objectif de fournir une librairie Python orientée objet permettant de simplifier,
standardiser et fiabiliser les appels HTTP(S) vers des API web REST.

### 2.3 Problématique

Les appels vers des API REST nécessitent souvent de gérer de manière répétitive :
- la construction des URLs ;
- les paramètres de requête ;
- les en-têtes HTTP ;
- l'authentification ;
- les timeouts ;
- les erreurs HTTP et réseau ;
- la sérialisation et le décodage des réponses ;
- la pagination ;
- le throttling et le retry ;
- le téléchargement de ressources distantes.

La librairie doit proposer une base claire, testable et extensible pour mutualiser ces besoins.

### 2.4 Périmètre

Le projet couvre :
- le développement d'une librairie Python distribuable ;
- une architecture orientée classes et composition ;
- un socle de transport HTTP(S) synchrone ;
- des stratégies d'authentification ;
- une façade de service ;
- la gestion des erreurs, du retry, du throttling et de la pagination ;
- la documentation développeur et utilisateur ;
- les tests unitaires et la configuration qualité.

Le projet ne couvre pas en V1 :
- la génération automatique de code depuis une spécification OpenAPI ;
- un client asynchrone ;
- des intégrations spécifiques à une API métier ;
- une interface graphique ou une CLI dédiée ;
- des mécanismes avancés d'orchestration distribuée.

---

## 3. Objectifs du projet

### 3.1 Objectif principal

Fournir une librairie Python générique permettant d'appeler des services REST avec un code clair,
réutilisable, robuste et maintenable.

### 3.2 Objectifs secondaires

Le projet doit permettre de :
- centraliser la logique d'appel HTTP(S) ;
- séparer clairement les responsabilités entre transport, authentification et service ;
- éviter les duplications de code dans les appels API ;
- proposer une architecture facilement testable ;
- offrir une hiérarchie d'exceptions cohérente ;
- faciliter la prise en charge d'API imposant pagination, limitations de débit, headers et règles
  de réponse spécifiques ;
- garantir une haute qualité logicielle via tests, typage strict et outillage qualité.

---

## 4. Principes directeurs d'architecture

### 4.1 Principe général

L'architecture du projet doit reposer prioritairement sur la **composition** et non sur une
hiérarchie d'héritage complexe.

### 4.2 Conséquences attendues

Le projet doit éviter une architecture du type :
- classe HTTP de base ;
- sous-classe sécurisée ;
- sous-classes spécialisées par verbe HTTP ;
- multiplication de sous-classes combinatoires.

Le projet doit préférer :
- un contrat d'appel HTTP central ;
- des objets de configuration ;
- des stratégies d'authentification ;
- des composants spécialisés et composables.

### 4.3 Bénéfices recherchés

L'architecture retenue doit améliorer :
- la lisibilité ;
- la testabilité ;
- l'extensibilité ;
- la maintenabilité ;
- la spécialisation progressive de la librairie.

---

## 5. Exigences fonctionnelles

### 5.1 Fonctionnalités principales

La librairie doit permettre :
- d'exécuter des appels HTTP(S) vers des services REST ;
- de construire proprement une requête à partir d'une base URL, d'un chemin et de paramètres ;
- de gérer les verbes HTTP standards ;
- d'ajouter des en-têtes par défaut et spécifiques à une requête ;
- d'appliquer une stratégie d'authentification ;
- de configurer un timeout ;
- de décoder les réponses textuelles et JSON ;
- de gérer les erreurs HTTP et réseau ;
- de rejouer certains appels selon une politique de retry ;
- de limiter la fréquence d'appel selon une politique de throttling ;
- d'exploiter des réponses paginées ;
- de télécharger des ressources distantes en streaming.

### 5.2 Fonctionnalités attendues en V1

La version initiale doit inclure a minima :
- support synchrone des méthodes `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD` et `OPTIONS` ;
- support des paramètres de requête ;
- support des headers ;
- support des corps JSON ;
- support d'une authentification de type :
  - aucune ;
  - Bearer ;
  - Basic ;
  - API key dans les headers ;
  - API key dans les query params ;
- gestion standardisée des réponses ;
- hiérarchie d'exceptions projet ;
- politique de retry simple ;
- politique de throttling simple ;
- support d'une pagination par URL de page suivante ;
- composant de téléchargement de fichier distant.

### 5.3 Fonctionnalités non retenues en V1

Les éléments suivants peuvent être étudiés ultérieurement mais ne sont pas exigés pour la V1 :
- transport asynchrone ;
- génération de code client ;
- sérialisation avancée de modèles métier ;
- gestion native multipart complexe ;
- cache HTTP avancé ;
- middlewares dynamiques arbitraires.

---

## 6. Exigences de conception

### 6.1 Contrat d'appel HTTP

Le projet doit définir une classe abstraite centrale nommée `BaobabWebApiCaller`.

Cette classe doit :
- représenter le contrat bas niveau d'exécution d'une requête HTTP(S) ;
- exposer une méthode abstraite de type `call(request: BaobabRequest) -> BaobabResponse` ;
- ne pas contenir de logique métier spécifique à une API donnée.

### 6.2 Objet de requête

Le projet doit définir un objet `BaobabRequest` permettant de modéliser une requête HTTP de manière
explicite, typée et testable.

Cet objet doit pouvoir contenir au minimum :
- la méthode HTTP ;
- le chemin relatif ;
- les query params ;
- les headers ;
- un corps JSON éventuel ;
- un corps de formulaire éventuel ;
- un timeout éventuel.

Le champ `BaobabRequest.query_params` supporte :
- une valeur `str` pour une clé unique ;
- une `Sequence[str]` pour représenter des clés répétées dans la query string.

### 6.3 Objet de réponse

Le projet doit définir un objet `BaobabResponse` normalisant les données de réponse.

Cet objet doit pouvoir exposer au minimum :
- le code HTTP ;
- les headers ;
- le contenu texte ;
- le contenu binaire brut ;
- un contenu JSON déjà décodé ou décodable.

### 6.4 Verbes HTTP

Les verbes HTTP ne doivent pas être modélisés comme une hiérarchie de classes dédiée.

Le projet doit utiliser :
- un `Enum` nommé `HttpMethod` ;
- des méthodes de confort au niveau service.

Les verbes à supporter sont :
- `GET`
- `POST`
- `PUT`
- `PATCH`
- `DELETE`
- `HEAD`
- `OPTIONS`

### 6.5 Authentification

Le projet doit gérer l'authentification via une stratégie dédiée et composable.

Il doit exister une abstraction `AuthenticationStrategy` avec des implémentations concrètes.

Les implémentations minimales attendues sont :
- `NoAuthenticationStrategy`
- `BearerAuthenticationStrategy`
- `BasicAuthenticationStrategy`
- `ApiKeyHeaderAuthenticationStrategy`
- `ApiKeyQueryAuthenticationStrategy`

### 6.6 Configuration de service

Le projet doit définir un objet `ServiceConfig` contenant les éléments de configuration communs à
un service distant.

Cet objet doit pouvoir centraliser au minimum :
- la base URL ;
- les headers par défaut ;
- la stratégie d'authentification ;
- le timeout par défaut ;
- la politique de retry ;
- la politique de throttling.

### 6.7 Façade de service

Le projet doit définir une classe `BaobabServiceCaller`.

Cette classe doit :
- encapsuler une configuration de service ;
- s'appuyer sur une instance de `BaobabWebApiCaller` ;
- construire les requêtes à partir de données métier ;
- exposer des méthodes de confort d'appel HTTP ;
- servir de base pour des services spécifiques.

### 6.8 Gestion des erreurs

Le projet doit prévoir un composant chargé de transformer les réponses en erreur en exceptions
métier du projet, en exposant un contexte HTTP utile au diagnostic (code, extrait de body texte,
certaines métadonnées, et un message lisible de type `HTTP {status_code} {raison}` quand la
raison standard est connue).

Ce composant doit permettre de mapper au minimum :
- les erreurs de configuration ;
- les erreurs de transport ;
- les timeouts ;
- les erreurs d'authentification ;
- les erreurs HTTP client ;
- les erreurs HTTP serveur ;
- les erreurs de limitation de débit ;
- les erreurs de décodage de réponse.

### 6.9 Pagination

Le projet doit fournir une brique dédiée à l'exploitation des réponses paginées, y compris lorsque
la query string comporte des paramètres multi-valués.

Cette brique doit permettre :
- d'extraire les éléments d'une page ;
- de déterminer s'il existe une page suivante ;
- d'obtenir l'URL de la page suivante ;
- d'itérer sur plusieurs pages.

### 6.10 Téléchargement de fichiers

Le projet doit fournir un composant dédié au téléchargement de fichiers distants en streaming.

Cette fonctionnalité doit être séparée de la simple consommation de réponses JSON afin de respecter
le principe de responsabilité unique.

---

## 7. Exigences non fonctionnelles

### 7.1 Maintenabilité

Le code doit être lisible, modulaire, documenté et structuré de manière à faciliter son évolution.

### 7.2 Testabilité

Chaque composant doit être conçu pour être testé indépendamment.

### 7.3 Extensibilité

La librairie doit permettre l'ajout futur de nouvelles stratégies d'authentification, de nouveaux
mécanismes de pagination ou de nouvelles politiques de résilience sans remise en cause du socle.

### 7.4 Robustesse

Le projet doit gérer proprement les erreurs attendues du réseau, du protocole HTTP, du décodage de
réponse et de la configuration.

### 7.5 Portabilité

Le projet doit être conçu pour être utilisable comme dépendance Python standard distribuée via un
packaging moderne basé sur `pyproject.toml`.

### 7.6 Qualité

Le projet doit respecter les règles de qualité définies dans les contraintes de développement,
notamment en matière de typage, tests, sécurité, linting et formatage.

---

## 8. Contraintes de développement à respecter

Les contraintes suivantes sont obligatoires pour le projet.

### 8.1 Structure du projet

L'arborescence doit respecter les principes suivants :
- le code source doit être dans `src/baobab_web_api_caller` ;
- les tests doivent être dans `tests/baobab_web_api_caller` ;
- la documentation de développement doit être dans `docs/`.

### 8.2 Une classe par fichier

Chaque classe doit être définie dans son propre fichier.

### 8.3 Arborescence logique

Les classes doivent être regroupées par domaines fonctionnels cohérents.

### 8.4 Exceptions spécifiques au projet

Toutes les exceptions spécifiques au projet doivent hériter d'une exception racine du projet.

### 8.5 Tests unitaires

Les exigences suivantes sont obligatoires :
- un fichier de tests par classe ;
- une classe de tests par fichier ;
- nommage `TestNomClasse` ;
- méthodes de tests `test_<nom>` ;
- arborescence miroir entre `src/` et `tests/` ;
- création d'une implémentation concrète dans les tests pour toute classe abstraite.

### 8.6 Couverture de code

La couverture minimale exigée est de **90%**.

Les fichiers liés à la couverture doivent être générés dans `docs/tests/coverage`.

### 8.7 Qualité et outillage

Le code doit passer sans erreur :
- `black` ;
- `pylint` ;
- `mypy` ;
- `flake8` ;
- `bandit`.

### 8.8 Longueur des lignes

La longueur maximale des lignes est fixée à **100 caractères**.

### 8.9 Configuration centralisée

Toutes les configurations possibles doivent être centralisées dans `pyproject.toml`.

### 8.10 Documentation

Toutes les classes et méthodes publiques doivent contenir des docstrings.

Le format recommandé est **reStructuredText**.

### 8.11 Journal de développement

Le projet doit maintenir un journal de développement dans `docs/dev_diary.md`.

### 8.12 Typage

Toutes les fonctions, méthodes, attributs et structures publiques doivent être annotés.

### 8.13 Versioning

Le projet doit suivre le **Semantic Versioning**.

### 8.14 Dépendances

Les dépendances de production et de développement doivent être séparées dans `pyproject.toml`.

### 8.15 Git workflow

Le projet doit suivre un workflow Git basé sur :
- branches dédiées ;
- Conventional Commits ;
- revue avant fusion.

---

## 9. Arborescence cible

```text
src/baobab_web_api_caller/
├── __init__.py
├── auth/
│   ├── __init__.py
│   ├── authentication_strategy.py
│   ├── no_authentication_strategy.py
│   ├── bearer_authentication_strategy.py
│   ├── basic_authentication_strategy.py
│   ├── api_key_header_authentication_strategy.py
│   └── api_key_query_authentication_strategy.py
├── config/
│   ├── __init__.py
│   ├── service_config.py
│   ├── retry_policy.py
│   ├── rate_limit_policy.py
│   └── default_header_provider.py
├── core/
│   ├── __init__.py
│   ├── baobab_web_api_caller.py
│   ├── baobab_request.py
│   ├── baobab_response.py
│   ├── http_method.py
│   ├── response_decoder.py
│   ├── json_response_decoder.py
│   ├── error_response_mapper.py
│   └── request_url_builder.py
├── download/
│   ├── __init__.py
│   └── bulk_file_downloader.py
├── exceptions/
│   ├── __init__.py
│   ├── baobab_web_api_caller_exception.py
│   ├── configuration_exception.py
│   ├── transport_exception.py
│   ├── timeout_exception.py
│   ├── authentication_exception.py
│   ├── http_exception.py
│   ├── client_http_exception.py
│   ├── server_http_exception.py
│   ├── resource_not_found_exception.py
│   ├── rate_limit_exception.py
│   ├── response_decoding_exception.py
│   └── service_call_exception.py
├── pagination/
│   ├── __init__.py
│   ├── page_result.py
│   ├── page_extractor.py
│   ├── next_page_url_extractor.py
│   └── paginator.py
├── service/
│   ├── __init__.py
│   └── baobab_service_caller.py
└── transport/
    ├── __init__.py
    ├── http_transport_caller.py
    └── requests_session_factory.py
```

---

## 10. Description des composants attendus

### 10.1 Couche `core`

#### `BaobabWebApiCaller`
Contrat abstrait d'exécution des requêtes.

#### `BaobabRequest`
Modélisation d'une requête HTTP.

#### `BaobabResponse`
Modélisation normalisée d'une réponse HTTP.

#### `HttpMethod`
Enum centralisant les verbes HTTP supportés.

#### `RequestUrlBuilder`
Composant chargé de construire l'URL finale à partir de la base URL, du path et des paramètres.

#### `ResponseDecoder`
Abstraction du décodage des réponses.

#### `JsonResponseDecoder`
Implémentation spécialisée pour le JSON.

#### `ErrorResponseMapper`
Transformation des erreurs HTTP et de contenu en exceptions du projet.

### 10.2 Couche `auth`

#### `AuthenticationStrategy`
Contrat d'application d'un mécanisme d'authentification à une requête.

#### Stratégies concrètes
Chaque stratégie concrète est responsable d'un unique mode d'authentification.

### 10.3 Couche `config`

#### `ServiceConfig`
Objet de configuration immuable ou quasi immuable d'un service distant.

#### `RetryPolicy`
Définition des règles de nouvelle tentative.

#### `RateLimitPolicy`
Définition des règles minimales de temporisation entre appels.

#### `DefaultHeaderProvider`
Fusion des en-têtes par défaut du service avec ceux de la requête (les valeurs de la requête
l'emportent pour une même clé). L'assemblage final avec la stratégie d'authentification est
effectué exclusivement dans `build_call_context` (transport), qui peut encore définir ou écraser
des clés comme `Authorization`.

### 10.4 Couche `transport`

#### `HttpTransportCaller`
Implémentation concrète du contrat d'appel HTTP.
Le composant applique le throttling, le retry configuré, le mapping des erreurs HTTP via
`ErrorResponseMapper` et la fermeture explicite des ressources `requests` (session/réponse).

#### `RequestsSessionFactory`
Factory de création de session HTTP synchrone.

### 10.5 Couche `service`

#### `BaobabServiceCaller`
Façade de service et point d'entrée haut niveau. Ne fusionne pas les en-têtes avec la
configuration : cette étape est réservée au transport (`build_call_context`).

### 10.6 Couche `pagination`

#### `PageResult`
Objet représentant une page de résultat.

#### `PageExtractor`
Extraction des informations de pagination depuis une réponse.

#### `NextPageUrlExtractor`
Extraction de l'URL de page suivante.

#### `Paginator`
Itération sur les pages d'une collection paginée.

### 10.7 Couche `download`

#### `BulkFileDownloader`
Téléchargement streaming d'un fichier distant.

### 10.8 Couche `exceptions`

La hiérarchie d'exceptions doit être propre au projet et refléter les grands domaines d'erreurs.

---

## 11. Hiérarchie d'exceptions attendue

```text
BaobabWebApiCallerException
├── ConfigurationException
├── TransportException
│   └── TimeoutException
├── AuthenticationException
├── HttpException
│   ├── ClientHttpException
│   │   ├── ResourceNotFoundException
│   │   └── RateLimitException
│   └── ServerHttpException
├── ResponseDecodingException
└── ServiceCallException
```

### 11.1 Règles associées

- toute exception spécifique au projet doit dériver de `BaobabWebApiCallerException` ;
- les messages d'erreur doivent être explicites ;
- les exceptions doivent transporter les informations utiles au diagnostic sans exposer de détails
  inutiles ;
- les erreurs de bibliothèques tierces doivent être encapsulées dans les exceptions du projet.

---

## 12. Organisation des tests

## 12.1 Arborescence cible des tests

```text
tests/baobab_web_api_caller/
├── auth/
├── config/
├── core/
├── download/
├── exceptions/
├── pagination/
├── service/
├── transport/
└── utils/
```

## 12.2 Règles de conception des tests

Les tests doivent respecter les règles suivantes :
- un fichier de test miroir `test_<nom_du_module>.py` pour chaque module `nom_du_module.py` sous
  `src/baobab_web_api_caller` (hors `__init__.py`) ; dans ce projet, chaque module source contient en
  pratique une seule classe publique, ce qui revient à « un fichier de test par classe » ;
- exceptions documentées : `call_context_builder.py` → `test_call_context_builder.py` pour
  `build_call_context` et `test_call_context.py` pour `CallContext` ; `mapping_utils.py` (fonctions) →
  `test_mapping_utils.py` ;
- une classe de tests dédiée par fichier (ex. `TestAuthenticationStrategy`) ;
- pour chaque classe abstraite, une implémentation concrète minimale dans le même fichier de test ;
- des tests unitaires isolés/déterministes ; une couverture minimale de 90 % ;
- pas de fichier agrégé unique pour plusieurs classes d’exceptions (ex. pas de `test_http_exceptions.py`) :
  un fichier par classe d’exception.

## 12.3 Tests minimaux à prévoir

Le projet doit inclure au minimum des tests pour :
- la construction d'une requête ;
- la construction d'une URL finale ;
- l'application des headers par défaut ;
- l'application de chaque stratégie d'authentification ;
- la gestion des timeouts ;
- le mapping des erreurs HTTP en exceptions projet ;
- le décodage JSON valide et invalide ;
- la politique de retry ;
- la politique de throttling ;
- l'itération sur une pagination ;
- le téléchargement de fichier ;
- la façade `BaobabServiceCaller` ;
- les classes abstraites via implémentations concrètes de test.

---

## 13. Documentation attendue

Le projet doit fournir les éléments suivants :
- `README.md` à la racine ;
- `CHANGELOG.md` à la racine ;
- `docs/dev_diary.md` ;
- documentation interne par docstrings ;
- exemples d'utilisation simples.

### 13.1 Contenu attendu du README

Le `README.md` doit contenir au minimum :
- une présentation du projet ;
- les prérequis ;
- les instructions d'installation ;
- un exemple minimal d'utilisation ;
- un exemple avec authentification ;
- un exemple avec pagination ;
- des indications de contribution ;
- la licence.

### 13.2 Documentation technique interne

La documentation interne doit expliquer :
- l'architecture ;
- les couches ;
- les responsabilités ;
- les conventions de développement ;
- les choix de conception importants.

---

## 14. Configuration et packaging

### 14.1 Fichier `pyproject.toml`

Le projet doit utiliser `pyproject.toml` comme fichier central de configuration.

### 14.2 Contenus attendus de `pyproject.toml`

Le fichier doit contenir ou configurer au minimum :
- métadonnées du projet ;
- version ;
- dépendances de production ;
- dépendances de développement ;
- configuration `black` ;
- configuration `pylint` ;
- configuration `mypy` ;
- configuration `flake8` ;
- configuration `bandit` ;
- configuration `pytest` ;
- configuration `coverage`.

### 14.3 Dépendances

Les dépendances doivent être limitées, justifiées et choisies pour préserver la lisibilité,
la sécurité et la maintenabilité de la librairie.

---

## 15. Phasage de développement recommandé

### Phase 1 - Socle projet

Objectifs :
- initialiser le projet ;
- mettre en place `pyproject.toml` ;
- créer l'arborescence ;
- créer l'exception racine ;
- créer `HttpMethod`, `BaobabRequest` et `BaobabResponse`.

### Phase 2 - Authentification et configuration

Objectifs :
- créer `AuthenticationStrategy` et ses implémentations ;
- créer `RetryPolicy` ;
- créer `RateLimitPolicy` ;
- créer `ServiceConfig` ;
- créer `DefaultHeaderProvider`.

### Phase 3 - Transport HTTP

Objectifs :
- créer `BaobabWebApiCaller` ;
- créer `RequestUrlBuilder` ;
- créer `RequestsSessionFactory` ;
- créer `HttpTransportCaller`.

### Phase 4 - Réponses et erreurs

Objectifs :
- créer `ResponseDecoder` ;
- créer `JsonResponseDecoder` ;
- créer `ErrorResponseMapper` ;
- finaliser les exceptions spécialisées.

### Phase 5 - Service haut niveau

Objectifs :
- créer `BaobabServiceCaller` ;
- exposer les méthodes de confort par verbe HTTP.

### Phase 6 - Pagination

Objectifs :
- créer `PageResult` ;
- créer `PageExtractor` ;
- créer `NextPageUrlExtractor` ;
- créer `Paginator`.

### Phase 7 - Téléchargement

Objectifs :
- créer `BulkFileDownloader` ;
- sécuriser le téléchargement streaming ;
- tester la robustesse de cette brique.

### Phase 8 - Documentation et stabilisation

Objectifs :
- finaliser le `README.md` ;
- finaliser le `CHANGELOG.md` ;
- compléter le journal de développement ;
- améliorer la couverture ;
- préparer la première release.

---

## 16. Critères d'acceptation

Le projet sera considéré conforme lorsque les conditions suivantes seront réunies :
- l'arborescence cible est en place ;
- chaque classe dispose de son fichier ;
- l'ensemble des composants obligatoires est implémenté ;
- la hiérarchie d'exceptions projet est respectée ;
- les tests unitaires atteignent au moins 90% de couverture ;
- tous les outils qualité passent sans erreur ;
- les docstrings publiques sont présentes ;
- le `README.md` et le `CHANGELOG.md` existent ;
- le journal `docs/dev_diary.md` est présent et correctement structuré ;
- le package est installable et importable ;
- une utilisation basique en service REST est démontrable.

---

## 17. Risques et points de vigilance

Les points suivants devront faire l'objet d'une attention particulière :
- dérive vers une hiérarchie de classes trop profonde ;
- couplage excessif entre transport et logique métier ;
- faible qualité du typage ;
- sous-couverture de tests ;
- gestion incomplète des erreurs externes ;
- dépendance trop forte à un backend HTTP précis ;
- explosion des dépendances ;
- manque de clarté de la documentation utilisateur.

---

## 18. Livrables attendus

Les livrables minimaux du projet sont :
- le code source du package ;
- le fichier `pyproject.toml` ;
- les tests unitaires ;
- le `README.md` ;
- le `CHANGELOG.md` ;
- le `docs/dev_diary.md` ;
- les rapports de couverture dans `docs/tests/coverage` ;
- la première version publiable de la librairie.

---

## 19. Conclusion

Le projet `baobab-web-api-caller` doit aboutir à une librairie Python générique, modulaire et
robuste dédiée à la simplification des appels vers des API REST.

Le développement doit concilier :
- simplicité d'utilisation ;
- rigueur architecturale ;
- qualité logicielle ;
- extensibilité ;
- conformité stricte aux contraintes de développement définies pour le projet.

Ce cahier des charges constitue la référence de développement pour la mise en oeuvre du projet.
