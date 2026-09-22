# NetOps Gateway

### Automated network health & compliance monitoring for hybrid enterprise networks — built on Cisco Meraki, FastAPI/Flask, Azure, Bash and Python.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

NetOps Gateway is a network operations platform that brings cloud telemetry, on-premises discovery, compliance checks, and operational visibility together in one workflow. It is designed to help network teams understand what is happening across distributed environments before outages, configuration drift, or compliance gaps become larger problems.

## Project Overview

NetOps Gateway collects live device data from Cisco Meraki, evaluates network health and compliance, and exposes the results through a secure REST API. 

The project is inspired by the topology-first experience of networking tools such as Cisco Packet Tracer: it connects the major components of a hybrid network into one easy-to-understand operational picture.

## Architecture Overview

<p align="center">
  <img src="docs/architecture.svg" alt="NetOps Gateway architecture overview showing Meraki Cloud, the FastAPI gateway, operations console, on-premises network, Bash and Python scripting and Cisco Packet Tracer lab" width="980">
</p>

<p align="center"><em>Cloud telemetry, compliance logic, on-premises scanning, and network-lab workflows connected through NetOps Gateway.</em></p>

## What It Does

- Collects live device and network data from Cisco Meraki
- Evaluates health, compliance, drift, and configuration state
- Provides secure FastAPI REST endpoints for operational visibility
- Supports Azure-ready deployment for hosted operations
- Has own CLI like Ansible and Terraform and other similar network automation platforms
- Connects network-lab and simulation workflows with real operational concepts

## Use Cases

- Track network health across branch, campus, retail, and hybrid environments
- Validate device and configuration compliance against internal standards
- Detect outage risk, configuration drift, and mismatched operational state
- Give network operations teams a centralized view of distributed infrastructure
- Prototype and visualize network behavior with Cisco Packet Tracer

## Technology Stack

- Python
- FastAPI/Flask
- Cisco Meraki API
- Azure
- Bash
- RESTful service architecture
- Cisco Packet Tracer for network modeling and simulation

## Repository Layout

- `docs/architecture.svg` — project architecture overview
- `README.md` — project overview and usage guidance
- Backend services — API and compliance logic
- Azure Cloud Platform - Free Tier resources
- Lab / simulation assets — Cisco Packet Tracer or model-based network workflows

## Getting Started

1. Configure Cisco Meraki API credentials and Azure environment settings.
2. Deploy the FastAPI/Flask backend in Azure or a local development environment.
3. Launch Azure App Services, serverless architecture with many configuration and optimization settings 
4. Query the API for device health, compliance status, and network insights.


## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Security

Please review [SECURITY.md](SECURITY.md) for supported versions and reporting procedures for vulnerabilities.

Built to mirror modern enterprise network operations.
