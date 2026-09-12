from __future__ import annotations

import importlib.util
import socket
import sys
from pathlib import Path

CHECKS = []


def check(name: str, ok: bool, detail: str) -> None:
    CHECKS.append(ok)
    mark = "✓" if ok else "✗"
    print(f"{mark} {name}: {detail}")


root = Path(__file__).resolve().parents[1]
check("Python", sys.version_info >= (3, 13), sys.version.split()[0])
check("Repository", (root / "apps/api").exists() and (root / "apps/web").exists(), str(root))
check("FastAPI", importlib.util.find_spec("fastapi") is not None, "installed" if importlib.util.find_spec("fastapi") else "missing")
check("SQLAlchemy", importlib.util.find_spec("sqlalchemy") is not None, "installed" if importlib.util.find_spec("sqlalchemy") else "missing")

for name, host, port in [
    ("PostgreSQL", "127.0.0.1", 5432),
    ("Redis", "127.0.0.1", 6379),
    ("NATS", "127.0.0.1", 4222),
]:
    try:
        with socket.create_connection((host, port), timeout=0.4):
            check(name, True, f"{host}:{port} reachable")
    except OSError:
        check(name, False, f"{host}:{port} not reachable (start docker compose for full stack)")

if not all(CHECKS[:4]):
    raise SystemExit(1)
