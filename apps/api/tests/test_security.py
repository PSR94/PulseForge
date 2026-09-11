import pytest

from pulseforge.services.security import UnsafeUrlError, validate_public_url


@pytest.mark.parametrize(
    "url",
    [
        "http://127.0.0.1/admin",
        "http://10.0.0.1/internal",
        "http://169.254.169.254/latest/meta-data",
        "file:///etc/passwd",
        "http://localhost:8000",
    ],
)
def test_blocks_ssrf_destinations(url):
    with pytest.raises(UnsafeUrlError):
        validate_public_url(url, resolve_dns=False)


def test_allows_public_literal_ip_without_dns():
    assert validate_public_url("https://1.1.1.1/feed", resolve_dns=False)
