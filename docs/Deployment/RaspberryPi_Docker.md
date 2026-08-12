# Raspberry Pi 5 Docker Demo

Use this path when the Mac cannot run a modern Docker Desktop version. The Raspberry Pi 5 can host the Docker stack, and the Mac can access the dashboard in a browser over the local network.

## Assumptions

- Raspberry Pi 5 is on the same network as the Mac.
- Docker and Docker Compose work on the Pi.
- The project files are available on the Pi by `git clone`, `git pull`, or a copied project folder.

## Run On The Pi

From the Raspberry Pi terminal:

```bash
cd ~/GovCaptureAI
./scripts/check-docker.sh
docker-compose up --build
```

The backend container waits for PostgreSQL and runs:

```bash
alembic upgrade head
```

## Open From The Mac

Find the Pi hostname or IP address:

```bash
hostname -I
```

Then open one of these from the Mac:

```text
Dashboard:   http://raspberrypi.local:8001
Backend API: http://raspberrypi.local:8000/docs
```

If `.local` does not resolve, use the Pi IP address:

```text
Dashboard:   http://<pi-ip-address>:8001
Backend API: http://<pi-ip-address>:8000/docs
```

The dashboard automatically points its API base to the same host on port `8000` when served over HTTP.

## Ports

- `8000`: FastAPI backend
- `8001`: dashboard frontend
- `5433`: PostgreSQL exposed on the Pi host, mapped to container port `5432`

## Stop Or Reset

Stop services:

```bash
docker-compose down
```

Reset database volume:

```bash
docker-compose down -v
```

## Notes

- Keep `SAM_API_MODE=mock` for demo-safe runs unless you intentionally configure a live SAM.gov key on the Pi.
- Do not copy `backend/.env` into Git.
- If the browser cannot reach the API, confirm both `8000` and `8001` are reachable from the Mac and that the dashboard API base shows the Pi hostname/IP.
