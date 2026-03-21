# API publique stable — version 1.0.0

Ce document fige le **contrat de compatibilité** pour les versions **1.x.y** (Semantic Versioning).

## Règle générale

- Les symboles listés dans `baobab_web_api_caller.__all__` (et donc importables depuis
  `import baobab_web_api_caller as b` ou `from baobab_web_api_caller import …`) constituent la
  **surface publique stable**.
- **Ajouts** rétrocompatibles (nouveaux symboles optionnels, nouveaux paramètres avec défaut,
  nouvelles exceptions dérivées) sont autorisés dans les versions **mineures** `1.x`.
- Toute **suppression**, **renommage** ou **changement de comportement observable** d’un symbole
  listé ci-dessous nécessite une version **majeure** **2.0.0** (ou un bump majeur ultérieur).

## Symboles exportés (`__all__`)

| Symbole | Rôle |
|--------|------|
| `__version__` | Version du package (chaîne PEP 440). |
| `ApiKeyHeaderAuthenticationStrategy` | Auth par clé API en en-tête HTTP. |
| `ApiKeyQueryAuthenticationStrategy` | Auth par clé API en query string. |
| `AuthenticationException` | Erreur HTTP 401 typée. |
| `AuthenticationStrategy` | Contrat des stratégies d’authentification. |
| `BaobabRequest` | Modèle de requête HTTP typée. |
| `BaobabResponse` | Modèle de réponse HTTP typée. |
| `BaobabServiceCaller` | Façade de haut niveau (GET, POST, …). |
| `BaobabWebApiCaller` | Contrat abstrait d’exécution (`call`). |
| `BaobabWebApiCallerException` | Base des exceptions du projet. |
| `BasicAuthenticationStrategy` | Authentification HTTP Basic. |
| `BearerAuthenticationStrategy` | Authentification Bearer. |
| `BulkFileDownloader` | Téléchargement streaming de fichiers. |
| `ClientHttpException` | Erreur HTTP 4xx (hors cas spécialisés ci-dessous). |
| `ConfigurationException` | Erreur de configuration / paramètres invalides. |
| `HttpException` | Base des erreurs HTTP avec contexte enrichi. |
| `HttpMethod` | Enum des méthodes HTTP supportées. |
| `HttpTransportCaller` | Transport synchrone `requests` + retry + throttling. |
| `NextPageUrlExtractor` | Contrat d’extraction d’URL de page suivante. |
| `NoAuthenticationStrategy` | Absence d’authentification. |
| `PageExtractor` | Contrat d’extraction d’items d’une page. |
| `PageResult` | Résultat d’une page de pagination. |
| `Paginator` | Itération sur les pages via URL suivante. |
| `RateLimitException` | Erreur HTTP 429. |
| `RateLimitPolicy` | Politique de throttling côté client. |
| `RequestsSessionFactory` | Fabrique de `requests.Session` injectable. |
| `ResourceNotFoundException` | Erreur HTTP 404. |
| `ResponseDecodingException` | Erreur de décodage de réponse (ex. JSON). |
| `RetryPolicy` | Politique de nouvelle tentative. |
| `ServerHttpException` | Erreur HTTP 5xx. |
| `ServiceCallException` | Erreur d’appel de service (couche service). |
| `ServiceConfig` | Configuration d’un service distant. |
| `TimeoutException` | Timeout réseau / requête. |
| `TransportException` | Erreur de transport générique. |

## Hors contrat `__all__` (usage avancé)

Les sous-modules (`baobab_web_api_caller.transport`, `baobab_web_api_caller.core`, etc.) restent
importables pour extension ou débogage. Les classes **non** listées dans `__all__` (ex.
`ErrorResponseMapper`, `JsonResponseDecoder`, `DefaultHeaderProvider`, `build_call_context`) peuvent
évoluer sans bump majeur tant qu’elles ne sont pas promues dans `__all__`.

## Références

- `README.md` — démarrage, limites, exemples.
- `docs/00_dev_constraints.md` — conventions du dépôt.
- `CHANGELOG.md` — historique des versions.
