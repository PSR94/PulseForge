# Security architecture

PulseForge treats ingestion as hostile input.

- URLs are validated before network access and again after every redirect.
- Loopback, private, link-local, multicast and otherwise non-public targets are rejected.
- Downloads are bounded and content types are allow-listed.
- Browser clients never receive provider secrets.
- Workspace roles distinguish viewer, analyst and admin access.
- Local mode has an explicit local principal; production JWT mode requires a configured secret.
- Request IDs and structured logs avoid dumping source bodies or credentials.
- Rate limiting is enforced at the HTTP boundary; production deployments should use a Redis-backed
  adapter for multi-replica consistency.
- Security headers disable MIME sniffing, framing and unnecessary browser capabilities.

See `SECURITY.md` for disclosure and deployment guidance.
