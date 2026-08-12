# Demo Server Runbook

This runbook is for Sprint 10B: running GovCaptureAI on the Raspberry Pi 5 as a repeatable local demo server.

## Demo Target

Default Pi connection:

```text
User: elastrilla
Host: 192.168.1.51
Path: ~/GovCaptureAI
```

Do not store the Pi password in the repository.

## Demo Entry Points

GovCaptureAI can be opened from two different places during development:

```text
Mac local file:     file:///Users/enriquelastrilla/GovCaptureAI/frontend/index.html
Raspberry Pi demo:  http://192.168.1.51:8001
```

Use the Raspberry Pi URL for a shared buyer walkthrough. Use the Mac local file when quickly checking frontend changes before syncing to the Pi.

The dashboard sidebar includes a Demo environment panel. Before a demo, confirm:

- Frontend shows `Raspberry Pi demo`.
- Dashboard shows `http://192.168.1.51:8001`.
- API target shows `http://192.168.1.51:8000`.
- Data mode shows `Live API data`.
- Version matches the expected sprint build.

If the browser shows an old version, sync and redeploy the Pi before troubleshooting the UI.

## 1. Sync From The Mac

From the Mac, in the project root:

```bash
cd /Users/enriquelastrilla/GovCaptureAI
./scripts/sync-to-pi.sh
```

Override defaults if needed:

```bash
PI_HOST=192.168.1.51 PI_USER=elastrilla ./scripts/sync-to-pi.sh
```

## 2. Start Or Update The Demo Stack

From the Mac:

```bash
./scripts/deploy-pi.sh
```

This connects to the Pi, checks Docker, builds the containers, starts them in the background, and prints container status.

## 3. Verify From The Mac

```bash
./scripts/check-demo-server.sh
```

Or with a custom host:

```bash
./scripts/check-demo-server.sh 192.168.1.51
```

Expected URLs:

```text
Dashboard:   http://192.168.1.51:8001
Backend API: http://192.168.1.51:8000/docs
Health:      http://192.168.1.51:8000/health
```

The check script also verifies the expected frontend build marker. If it reports an outdated frontend, run:

```bash
./scripts/sync-to-pi.sh
./scripts/deploy-pi.sh
./scripts/check-demo-server.sh
```

## 4. Stop The Demo

SSH into the Pi:

```bash
ssh elastrilla@192.168.1.51
cd ~/GovCaptureAI
docker-compose down
```

## 5. Reset Demo Data

Use this only when you want a clean database:

```bash
ssh elastrilla@192.168.1.51
cd ~/GovCaptureAI
docker-compose down -v
docker-compose up --build -d
```

## Troubleshooting

- If `~/GovCaptureAI` does not exist on the Pi, run `./scripts/sync-to-pi.sh` from the Mac first.
- If Docker fails on the Mac, ignore it and run Docker only on the Pi.
- If the dashboard opens but data is offline, confirm the API base shows `http://192.168.1.51:8000`.
- If the dashboard opens but a new button or field is missing, confirm the Demo environment version first.
- If `raspberrypi.local` does not resolve, use `192.168.1.51`.
