# Security Policy

## Reporting

Please report security vulnerabilities privately through GitHub Security Advisories for this repository. Do not publish exploit details in a public issue before maintainers have had an opportunity to respond.

## Security boundaries

PulseForge treats remote ingestion as hostile input. URL connectors must reject loopback, link-local, RFC1918/private, multicast, and otherwise non-public destinations; redirects must be revalidated; downloads are bounded; content types are checked; and credentials must never be interpolated into fetched URLs or logs.

Provider secrets are server-side environment variables only. The web application receives the PulseForge API URL, never model-provider credentials.

Workspace identifiers are carried through domain and API boundaries. Production deployments should pair these checks with authenticated principals and row-level authorization in the persistence layer.
