# SOCIRIS Evidence Stack

A production-style local DevSecOps MVP demonstrating containerization, reverse proxying, health checks, persistent data, least privilege, and failure recovery.

## Architecture

Client → `127.0.0.1:8080` → Nginx → private Docker network → Python app on port `8004` → SQLite named volume
Only Nginx publishes a host port. The Python application remains internal to Docker.

## Features

- Two-service Docker Compose stack
- Nginx reverse proxy
- Python API and HTML frontend
- Persistent SQLite visit counter
- Application and proxy health checks
- Non-root application container
- Read-only application filesystem
- All application Linux capabilities dropped
- `no-new-privileges` enabled
- Graceful `SIGTERM` handling
- Bounded Nginx upstream timeouts
## Endpoints

- `/` — frontend
- `/health` — non-mutating health check
- `/api/visits` — increments and returns the persisted counter

## Run locally

Requirements: Docker Engine and Docker Compose v2.

1. Run `docker compose up --detach --build`
2. Check `docker compose ps`
3. Test `curl http://127.0.0.1:8080/health`
4. Test `curl http://127.0.0.1:8080/api/visits`
5. Stop with `docker compose down`

Stopping with `docker compose down` preserves the named volume unless `--volumes` is deliberately supplied.

## Verified behavior

- Healthy Nginx-to-application routing
- No application port published to the host
- SQLite persistence across container replacement
- Bounded gateway failure while the app was unavailable
- Graceful shutdown with exit code `0`
- Successful recovery

See `docs/verification.md` for the evidence narrative.
## Status

This is a verified local MVP, not yet an internet-facing production deployment. Continuous integration, automated security checks, HTTPS, and remote deployment remain roadmap items.
