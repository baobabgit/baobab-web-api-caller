"""Exemple minimal d'utilisation de BulkFileDownloader.

Imports depuis le package racine (contrat stable 1.0.0) ; voir `docs/v1.0.0/00_public_api.md`.
"""

from __future__ import annotations

from pathlib import Path

from baobab_web_api_caller import (
    BaobabRequest,
    BulkFileDownloader,
    HttpMethod,
    RequestsSessionFactory,
    ServiceConfig,
)


def main() -> None:
    cfg = ServiceConfig(base_url="https://example.com")
    downloader = BulkFileDownloader.from_service_config(
        service_config=cfg, session_factory=RequestsSessionFactory()
    )

    request = BaobabRequest(
        method=HttpMethod.GET, path="/files/report.pdf", query_params={}, headers={}
    )
    target = Path("report.pdf")
    _ = downloader.download(request, output_path=target, overwrite=True)


if __name__ == "__main__":
    main()
