from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse


class UnsafeUrlError(ValueError):
    pass


def _is_public_ip(value: str) -> bool:
    ip = ipaddress.ip_address(value)
    return not (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def validate_public_url(url: str, *, resolve_dns: bool = True) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise UnsafeUrlError("Only http and https URLs are allowed")
    if not parsed.hostname:
        raise UnsafeUrlError("URL must include a hostname")
    if parsed.username or parsed.password:
        raise UnsafeUrlError("Embedded credentials are not allowed")

    host = parsed.hostname.strip("[]")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        is_ip_literal = False
    else:
        is_ip_literal = True

    if is_ip_literal:
        if not _is_public_ip(host):
            raise UnsafeUrlError("Private or non-public IP destinations are not allowed")
        return url

    if host.lower() in {"localhost", "localhost.localdomain"} or host.lower().endswith(".local"):
        raise UnsafeUrlError("Local hostnames are not allowed")

    if resolve_dns:
        try:
            records = socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))
        except socket.gaierror as exc:
            raise UnsafeUrlError("Hostname could not be resolved") from exc
        for record in records:
            address = record[4][0]
            if not _is_public_ip(address):
                raise UnsafeUrlError("Hostname resolves to a private or non-public destination")
    return url
