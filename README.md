# Automated Incident Remediation & Observability Engine

An automated self-healing operational system using Python, FastAPI, Prometheus, Alertmanager, and Docker.

## Architecture
- **Target App (`app`)**: FastAPI microservice emitting Prometheus metrics.
- **Prometheus (`prometheus`)**: Scrapes `/metrics` every 2s and fires alerts based on error thresholds.
- **Alertmanager (`alertmanager`)**: Routes critical alerts to the Auto-Remediator webhook.
- **Auto-Remediator (`remediator`)**: Listens for alerts and triggers automated self-healing APIs.
- 


<img width="1652" height="537" alt="Screenshot 2026-10-16 171351" src="https://github.com/user-attachments/assets/642942c0-f71d-4584-84d1-a883c30e2bf0" />

## How to Run

```bash
docker compose up --build
```

## How to Test

1. Verify healthy status:
   `curl http://localhost:8000/`

2. Inject failure state:
   `curl http://localhost:8000/simulate-failure`

3. Trigger error rate:
   `curl http://localhost:8000/data`

4. Watch Prometheus & Alertmanager detect the issue and the remediator service automatically restore the application to a healthy state!
