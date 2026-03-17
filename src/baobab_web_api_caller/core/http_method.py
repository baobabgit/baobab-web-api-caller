"""Enum des méthodes HTTP supportées."""

from __future__ import annotations

from enum import Enum


class HttpMethod(str, Enum):
    """Méthodes HTTP supportées par la librairie."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
