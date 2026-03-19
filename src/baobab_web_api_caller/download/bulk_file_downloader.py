"""Téléchargement de fichiers distants en streaming."""

# pylint: disable=duplicate-code

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import requests

from baobab_web_api_caller.config.default_header_provider import DefaultHeaderProvider
from baobab_web_api_caller.config.service_config import ServiceConfig
from baobab_web_api_caller.core.baobab_request import BaobabRequest
from baobab_web_api_caller.core.baobab_response import BaobabResponse
from baobab_web_api_caller.core.error_response_mapper import ErrorResponseMapper
from baobab_web_api_caller.core.request_url_builder import RequestUrlBuilder
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException
from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from baobab_web_api_caller.exceptions.transport_exception import TransportException
from baobab_web_api_caller.transport.call_context_builder import build_call_context
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory


@dataclass(frozen=True, slots=True)
class BulkFileDownloader:
    """Télécharge une ressource distante vers le disque en streaming.

    Le downloader est séparé de la consommation classique (JSON) afin d'éviter de charger les
    contenus volumineux en mémoire.
    """

    service_config: ServiceConfig
    session_factory: RequestsSessionFactory
    url_builder: RequestUrlBuilder
    default_header_provider: DefaultHeaderProvider
    error_response_mapper: ErrorResponseMapper

    @classmethod
    def from_service_config(
        cls, service_config: ServiceConfig, session_factory: RequestsSessionFactory
    ) -> "BulkFileDownloader":
        """Construit un downloader à partir d'une configuration de service."""

        return cls(
            service_config=service_config,
            session_factory=session_factory,
            url_builder=RequestUrlBuilder(base_url=service_config.base_url),
            default_header_provider=DefaultHeaderProvider(
                default_headers=service_config.default_headers
            ),
            error_response_mapper=ErrorResponseMapper(),
        )

    def download(
        self,
        request: BaobabRequest,
        *,
        output_path: Path,
        chunk_size: int = 1024 * 64,
        overwrite: bool = False,
    ) -> Path:
        """Télécharge la ressource et l'écrit sur disque.

        L'écriture est effectuée dans un fichier temporaire puis renommée, afin d'éviter les
        fichiers partiels en cas d'erreur.

        La réponse streaming est fermée systématiquement en fin d'exécution (succès, erreur HTTP
        ou exception), afin d'éviter toute fuite de ressources.

        :param request: Requête à exécuter (souvent GET).
        :type request: BaobabRequest
        :param output_path: Chemin cible.
        :type output_path: Path
        :param chunk_size: Taille de chunk pour le streaming.
        :type chunk_size: int
        :param overwrite: Autorise l'écrasement du fichier cible.
        :type overwrite: bool
        :return: Chemin final.
        :rtype: Path
        :raises ConfigurationException: Si les paramètres sont invalides.
        :raises TimeoutException: En cas de timeout réseau.
        :raises HttpException: Si la réponse HTTP indique une erreur (4xx/5xx), mappée via
            `ErrorResponseMapper`.
        :raises TransportException: En cas d'erreur réseau ou d'écriture.
        """

        if request.json_body is not None or request.form_body is not None:
            raise ConfigurationException("download only supports requests without body")
        if chunk_size <= 0:
            raise ConfigurationException("chunk_size must be positive")

        output_path = Path(output_path)
        if output_path.exists() and not overwrite:
            raise TransportException("output_path already exists")

        ctx = None
        try:
            ctx = build_call_context(
                request=request,
                service_config=self.service_config,
                default_header_provider=self.default_header_provider,
                url_builder=self.url_builder,
                session_factory=self.session_factory,
            )
        except requests.Timeout as exc:  # pragma: no cover
            raise TimeoutException(str(exc)) from exc
        except requests.RequestException as exc:  # pragma: no cover
            raise TransportException(str(exc)) from exc

        if ctx is None:
            raise TransportException("call context was not built")

        response: requests.Response | None = None
        try:
            try:
                response = ctx.session.request(
                    method=ctx.prepared_request.method.value,
                    url=ctx.url,
                    params=None,
                    headers=dict(ctx.prepared_request.headers),
                    json=None,
                    data=None,
                    timeout=ctx.timeout,
                    stream=True,
                )
            except requests.Timeout as exc:  # pragma: no cover
                raise TimeoutException(str(exc)) from exc
            except requests.RequestException as exc:  # pragma: no cover
                raise TransportException(str(exc)) from exc

            try:
                headers: dict[str, str] = {str(k): str(v) for k, v in response.headers.items()}
                status = int(response.status_code)

                if status >= 400:
                    raw = BaobabResponse(
                        status_code=status, headers=headers, text=response.text, content=None
                    )
                    self.error_response_mapper.raise_for_error(raw)

                tmp_path = output_path.with_suffix(output_path.suffix + ".part")
                try:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with tmp_path.open("wb") as f:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if not chunk:
                                continue
                            f.write(chunk)
                    if overwrite and output_path.exists():
                        output_path.unlink()
                    tmp_path.replace(output_path)
                    return output_path
                except OSError as exc:
                    try:
                        if tmp_path.exists():
                            tmp_path.unlink()
                    except OSError:
                        pass
                    raise TransportException(str(exc)) from exc
            finally:
                if response is not None:
                    response.close()
        finally:
            if ctx is not None:
                ctx.session.close()
