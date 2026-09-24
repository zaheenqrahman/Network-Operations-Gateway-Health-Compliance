# NetOps Gateway

### Automated network health & compliance monitoring for enterprise networks — built on Cisco Meraki, Flask, and Azure.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

NetOps Gateway is a REST API that pulls live network and device data from the Cisco Meraki cloud, evaluates health and compliance against a simple rule set, and exposes the results as JSON. It's built to help a network operations team see device status, compliance gaps, and active alerts across an organization without digging through the Meraki dashboard by hand.

## Architecture Overview

<p align="center">
  <img src="docs/architecture.svg" alt="NetOps Gateway architecture overview showing Meraki Cloud feeding the Flask API gateway, which is queried by an operations console or client" width="980">
</p>

<p align="center"><em>Meraki Cloud telemetry flows into NetOps Gateway, which evaluates health/compliance and serves the results over REST.</em></p>

## What It Does

- Pulls live network and device data from the Cisco Meraki Dashboard API
- Evaluates network health based on live device status (online/offline/alerting)
- Checks individual devices against a compliance rule set (status + approved model list)
- Scans all networks for active alerts in one call
- Falls back to mock data automatically if the Meraki API is unreachable, so the API stays usable in demos/dev without live credentials — every response includes a `"source": "live" | "mock"` field so it's never ambiguous which one you're looking at

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/networks` | List all networks in the organization |
| GET | `/networks/<network_id>/health` | Health status of a specific network |
| GET | `/devices` | List all devices in the organization |
| GET | `/devices/<serial>/compliance` | Compliance check for a specific device |
| POST | `/alerts/scan` | Scan all networks and return active alerts |

## Technology Stack

- **Python / Flask** — REST API
- **Cisco Meraki Dashboard API** — live network/device telemetry
- **Azure App Service** — hosting, deployed via GitHub Actions CI/CD
- **pytest** — test suite for compliance and health logic

## Getting Started

1. Clone the repo and install dependencies: `pip install -r requirements.txt`
2. Set the `MERAKI_API_KEY` and `ORG_ID` environment variables (never hardcoded or committed — see [SECURITY.md](SECURITY.md))
3. Run locally with `python application.py`, or deploy to Azure App Service — the included GitHub Actions workflow (`.github/workflows/`) auto-deploys on push to `main` using `gunicorn --bind=0.0.0.0 --timeout 600 application:app` as the startup command
4. Query the API for network health, device compliance, and alerts

## Repository Layout

- `application.py` — Flask app, API routes, and compliance/health logic
- `tests/` — pytest test suite
- `docs/architecture.svg` — architecture diagram
- `.github/workflows/` — CI/CD pipeline (Azure deploy)
- `Cisco Packet Tracer` - Physical network topology layout with physical devices (servers, switches, computers) over cloud resources and physical infrastructure 

## Roadmap

- Real device compliance data — currently proven against a Cisco DevNet Meraki sandbox (populated with real devices); the production org has networks but no owned/claimed hardware yet, so `/devices` returns mock data there until a real or Systems-Manager-enrolled device is added
- Cisco Packet Tracer network topology lab — not yet built

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Security

Please review [SECURITY.md](SECURITY.md) for supported versions and reporting procedures for vulnerabilities.
