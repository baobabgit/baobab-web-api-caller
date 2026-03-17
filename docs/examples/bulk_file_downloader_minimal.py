"""Exemple minimal d'utilisation de BulkFileDownloader."""

from __future__ import annotations

from pathlib import Path

from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.download.bulk_file_downloader import BulkFileDownloader
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


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
