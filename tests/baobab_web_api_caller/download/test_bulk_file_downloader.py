"""Tests de `BulkFileDownloader`."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.http_method import HttpMethod
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException
from baobab_web_api_caller.exceptions.resource_not_found_exception import ResourceNotFoundException
from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from baobab_web_api_caller.exceptions.transport_exception import TransportException
from baobab_web_api_caller.download.bulk_file_downloader import BulkFileDownloader
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


@dataclass(frozen=True, slots=True)
class FakeSessionFactory(RequestsSessionFactory):
    """Factory de session injectant un mock."""

    session: requests.Session

    def create(self) -> requests.Session:
        """Retourne la session injectée."""

        return self.session


class TestBulkFileDownloader:
    """Tests unitaires du downloader."""

    def test_download_rejects_request_body(self, tmp_path: Path) -> None:
        """Refuse les requêtes avec body (download streaming uniquement)."""

        session = Mock(spec=requests.Session)
        cfg = ServiceConfig(base_url="https://example.com")
        downloader = BulkFileDownloader.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )

        out = tmp_path / "file.bin"
        req = BaobabRequest(
            method=HttpMethod.POST,
            path="/bin",
            query_params={},
            headers={},
            json_body={"a": 1},
        )

        with pytest.raises(ConfigurationException):
            downloader.download(req, output_path=out)

    def test_download_rejects_invalid_chunk_size(self, tmp_path: Path) -> None:
        """chunk_size doit être strictement positif."""

        session = Mock(spec=requests.Session)
        cfg = ServiceConfig(base_url="https://example.com")
        downloader = BulkFileDownloader.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )

        out = tmp_path / "file.bin"
        req = BaobabRequest(method=HttpMethod.GET, path="/bin", query_params={}, headers={})

        with pytest.raises(ConfigurationException):
            downloader.download(req, output_path=out, chunk_size=0)

    def test_download_streams_to_disk(self, tmp_path: Path) -> None:
        """Écrit le contenu itéré par chunks sur disque."""

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.headers = {"Content-Type": "application/octet-stream"}
        response.iter_content.return_value = [b"ab", b"", b"cd"]

        session = Mock(spec=requests.Session)
        session.request.return_value = response

        cfg = ServiceConfig(base_url="https://example.com")
        downloader = BulkFileDownloader.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )

        out = tmp_path / "file.bin"
        req = BaobabRequest(method=HttpMethod.GET, path="/bin", query_params={}, headers={})
        saved = downloader.download(req, output_path=out, chunk_size=2)

        assert saved == out
        assert out.read_bytes() == b"abcd"
        session.request.assert_called_once()
        assert session.request.call_args.kwargs["stream"] is True

    def test_download_raises_on_existing_file_when_no_overwrite(self, tmp_path: Path) -> None:
        """Refuse d'écraser un fichier existant par défaut."""

        session = Mock(spec=requests.Session)
        cfg = ServiceConfig(base_url="https://example.com")
        downloader = BulkFileDownloader.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )

        out = tmp_path / "file.bin"
        out.write_bytes(b"x")
        req = BaobabRequest(method=HttpMethod.GET, path="/bin", query_params={}, headers={})

        with pytest.raises(TransportException):
            downloader.download(req, output_path=out, overwrite=False)

    def test_download_overwrites_when_enabled(self, tmp_path: Path) -> None:
        """Écrase le fichier cible si overwrite=True."""

        response = Mock(spec=requests.Response)
        response.status_code = 200
        response.headers = {"Content-Type": "application/octet-stream"}
        response.iter_content.return_value = [b"new"]

        session = Mock(spec=requests.Session)
        session.request.return_value = response

        cfg = ServiceConfig(base_url="https://example.com")
        downloader = BulkFileDownloader.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )

        out = tmp_path / "file.bin"
        out.write_bytes(b"old")
        req = BaobabRequest(method=HttpMethod.GET, path="/bin", query_params={}, headers={})

        _ = downloader.download(req, output_path=out, overwrite=True)
        assert out.read_bytes() == b"new"

    def test_timeout_is_wrapped(self, tmp_path: Path) -> None:
        """Wrappe requests.Timeout en TimeoutException."""

        session = Mock(spec=requests.Session)
        session.request.side_effect = requests.Timeout("boom")

        cfg = ServiceConfig(base_url="https://example.com")
        downloader = BulkFileDownloader.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )

        out = tmp_path / "file.bin"
        req = BaobabRequest(method=HttpMethod.GET, path="/bin", query_params={}, headers={})

        with pytest.raises(TimeoutException):
            downloader.download(req, output_path=out)

    def test_http_error_is_mapped(self, tmp_path: Path) -> None:
        """Mappe une réponse HTTP en exception projet."""

        response = Mock(spec=requests.Response)
        response.status_code = 404
        response.headers = {}
        response.text = "not found"

        session = Mock(spec=requests.Session)
        session.request.return_value = response

        cfg = ServiceConfig(base_url="https://example.com")
        downloader = BulkFileDownloader.from_service_config(
            service_config=cfg, session_factory=FakeSessionFactory(session=session)
        )

        out = tmp_path / "file.bin"
        req = BaobabRequest(method=HttpMethod.GET, path="/missing", query_params={}, headers={})

        with pytest.raises(ResourceNotFoundException):
            downloader.download(req, output_path=out)
