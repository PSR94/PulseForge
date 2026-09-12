# Local development

```bash
git clone https://github.com/PSR94/PulseForge.git
cd PulseForge
cp .env.example .env
docker compose up --build
```

Open:
- Web: http://localhost:3000
- API docs: http://localhost:8000/docs
- NATS monitoring: http://localhost:8222
- Prometheus (optional profile): http://localhost:9090

Useful commands:

```bash
make doctor
make test
make backend-test
make frontend-test
make e2e
make migrate
make screenshots
```

The default workspace is deterministic and does not require a paid AI key. Add an RSS/JSON/web/GitHub/
arXiv/Hacker News source from the Sources screen and click **Ingest** to materialize live documents into
events and observational temporal graph state.
