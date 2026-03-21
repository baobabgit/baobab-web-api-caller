"""Exemple minimal d'utilisation de BaobabServiceCaller.

Préférez les imports depuis le package racine (contrat stable 1.0.0 ;
voir `docs/v1.0.0/00_public_api.md`).
"""

from __future__ import annotations

from baobab_web_api_caller import (
    BaobabServiceCaller,
    BearerAuthenticationStrategy,
    HttpTransportCaller,
    RequestsSessionFactory,
    ServiceConfig,
)


def main() -> None:
    cfg = ServiceConfig(
        base_url="https://example.com",
        authentication_strategy=BearerAuthenticationStrategy(token="token"),
    )
    transport = HttpTransportCaller.from_service_config(
        service_config=cfg, session_factory=RequestsSessionFactory()
    )
    service = BaobabServiceCaller(service_config=cfg, web_api_caller=transport)

    resp = service.get("/health")
    _ = resp.status_code


if __name__ == "__main__":
    main()
