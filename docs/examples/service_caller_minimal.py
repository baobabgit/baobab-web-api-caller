"""Exemple minimal d'utilisation de BaobabServiceCaller."""

from __future__ import annotations

from baobab_web_api_caller.auth.bearer_authentication_strategy import BearerAuthenticationStrategy
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.service.baobab_service_caller import BaobabServiceCaller
from baobab_web_api_caller.transport.http_transport_caller import HttpTransportCaller
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


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
