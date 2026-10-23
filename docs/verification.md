# Verification Evidence

Date: 2026-10-23
Environment: Local Ubuntu under WSL2
Scope: Local DevSecOps MVP

## Healthy-stack proof

The Docker Compose stack started two services:

- `app`: Python application on internal port 8004
- `proxy`: Nginx published only on `127.0.0.1:8080`

Both services reached Docker health status `healthy`.
Requests through Nginx returned:

- `/health` → `{"status": "ok"}`
- `/` → the expected Day 4 application page
- `/api/visits` → visit counts 1 and 2

Docker inspection returned empty application host bindings, proving that port 8004 was not published to the host.

## Persistence proof

The application container was forcibly recreated.

- Original and replacement container IDs differed.
- The visit counter continued at 3 after recreation.
- After another stop and start, it continued at 4.

This proves that SQLite data survived outside the replaceable application container in the named Docker volume.

## Failure and recovery proof

The first controlled stop exposed two genuine weaknesses:

- The application required Docker's forced kill and exited 137.
- Nginx waited too long for its unavailable upstream.

The application was updated to handle `SI
GTERM`, and bounded Nginx upstream timeouts were added.

The repeated test proved:

- Application stopped in 0 seconds.
- Application exited with code 0.
- Logs recorded the shutdown signal and graceful stop.
- Nginx returned HTTP 504 while the upstream was unavailable.
- Application restarted and returned healthy.
- Persistent data remained available.

## Current limitations

This proof is local and manually verified. CI, automated security scanning, HTTPS, remote deployment, monitoring, and backup automation remain future work.
