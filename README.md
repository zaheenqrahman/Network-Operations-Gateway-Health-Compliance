# NetOps Gateway

### Automated network health and compliance monitoring for hybrid enterprise networks — built on Cisco Meraki, FastAPI, Azure, and C++.

NetOps Gateway is a network operations platform that brings cloud telemetry, on-premises discovery, compliance checks, and operational visibility together in one workflow. It is designed to help network teams understand what is happening across distributed environments before an outage or configuration drift becomes a larger problem.

## Project Overview

NetOps Gateway collects live device data from Cisco Meraki, evaluates network health and compliance, and exposes the results through a secured REST API. A lightweight C++ scanner extends visibility into the on-premises environment, while Azure provides a path for hosted deployment.

The project is inspired by the visual, topology-first experience of tools such as Cisco Packet Tracer: it connects the major pieces of a hybrid network into one easy-to-understand operational picture.

## Architecture Overview

<p align="center">
  <img src="docs/architecture.svg" alt="NetOps Gateway architecture overview showing Meraki Cloud, the FastAPI gateway, operations console, on-premises network, C++ scanner, and Cisco Packet Tracer lab" width="980">
</p>

<p align="center"><em>Cloud telemetry, compliance logic, on-premises scanning, and network-lab workflows connected through NetOps Gateway.</em></p>

## What It Does

- Collects live device and network data from Cisco Meraki
- Evaluates health, compliance, drift, and configuration state
- Provides secure FastAPI REST endpoints for operational visibility
- Supports Azure-ready deployment for hosted operations
- Uses a lightweight C++ scanner for on-premises discovery and checks
- Connects network-lab and simulation workflows with real operational concepts

## Use Cases

- Track network health across branch, campus, and hybrid environments
- Validate device and configuration compliance against internal standards
- Detect outage risk, configuration drift, and mismatched operational state
- Give network operations teams a centralized view of distributed infrastructure
- Prototype and visualize network behavior with Cisco Packet Tracer

## Technology Stack

- Python
- FastAPI
- Cisco Meraki API
- Azure
- C++
- RESTful service architecture
- Cisco Packet Tracer for network modeling and simulation

## Getting Started

1. Configure Cisco Meraki API credentials and Azure environment settings.
2. Deploy the FastAPI backend in Azure or a local development environment.
3. Run the C++ scan tool on the on-premises network side.
4. Query the API for device health, compliance status, and network insights.

## Repository Layout

- `docs/architecture.svg` — project architecture overview
- FastAPI backend — API and compliance workflows
- C++ scanner — host-side discovery and checks
- Cisco Packet Tracer assets — network lab and simulation workflows

## License

This project is intended for internal network automation and operations workflows. Update the license terms to match your organization's policy before production use.

---

Built for modern enterprise network operations.
