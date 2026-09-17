# NetOps Gateway

### Automated network health & compliance monitoring for hybrid enterprise networks — built on Meraki, FastAPI, Azure, and C++.

NetOps Gateway is a REST API that automates network health and compliance checks across a hybrid enterprise network. It pulls live data from Cisco Meraki's cloud platform, applies custom compliance logic, and exposes it through a secured Python/FastAPI backend deployed on Azure — paired with a lightweight C++ scanning tool for the on-prem side.

Network automation API that pulls live device data from Meraki, applies health/compliance checks, and exposes it via a secured REST interface — with a C++ scan tool and Azure deployment.

## Overview

NetOps Gateway helps network teams monitor the health of hybrid environments by combining cloud telemetry from Meraki with a fast on-prem scan workflow. The platform validates device state, identifies drift from policy, and surfaces actionable compliance results through a secure API layer.

## Architecture

<div align="center">
  <svg width="980" height="430" viewBox="0 0 980 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="NetOps Gateway network diagram">
    <defs>
      <linearGradient id="bg" x1="0" x2="1">
        <stop offset="0%" stop-color="#071425"/>
        <stop offset="100%" stop-color="#0d1f33"/>
      </linearGradient>
      <linearGradient id="azure" x1="0" x2="1">
        <stop offset="0%" stop-color="#5cc8ff"/>
        <stop offset="100%" stop-color="#2e7df6"/>
      </linearGradient>
      <linearGradient id="meraki" x1="0" x2="1">
        <stop offset="0%" stop-color="#7ef0c3"/>
        <stop offset="100%" stop-color="#30b38a"/>
      </linearGradient>
      <linearGradient id="cpp" x1="0" x2="1">
        <stop offset="0%" stop-color="#ffe08a"/>
        <stop offset="100%" stop-color="#ffb347"/>
      </linearGradient>
      <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.25"/>
      </filter>
    </defs>

    <rect width="980" height="430" fill="url(#bg)" rx="18"/>

    <g font-family="Segoe UI, Arial, sans-serif">
      <rect x="40" y="65" width="260" height="110" rx="16" fill="#12283f" stroke="#4fb8ff" stroke-width="2" filter="url(#shadow)"/>
      <text x="170" y="106" text-anchor="middle" font-size="22" font-weight="700" fill="#eaf6ff">Meraki Cloud</text>
      <text x="170" y="136" text-anchor="middle" font-size="15" fill="#9ecae9">Live network telemetry</text>
      <rect x="88" y="155" width="164" height="12" rx="6" fill="url(#meraki)"/>
      <circle cx="92" cy="147" r="8" fill="#7ef0c3"/>
      <circle cx="120" cy="147" r="8" fill="#7ef0c3" opacity="0.8"/>
      <circle cx="148" cy="147" r="8" fill="#7ef0c3" opacity="0.65"/>
      <circle cx="176" cy="147" r="8" fill="#7ef0c3" opacity="0.8"/>
      <circle cx="204" cy="147" r="8" fill="#7ef0c3"/>

      <rect x="358" y="90" width="260" height="160" rx="18" fill="#152d4d" stroke="#72d5ff" stroke-width="2" filter="url(#shadow)"/>
      <text x="488" y="126" text-anchor="middle" font-size="22" font-weight="700" fill="#eaf6ff">NetOps Gateway</text>
      <text x="488" y="154" text-anchor="middle" font-size="15" fill="#9ecae9">FastAPI + Compliance Engine</text>
      <rect x="404" y="176" width="168" height="12" rx="6" fill="url(#azure)"/>
      <rect x="404" y="198" width="142" height="12" rx="6" fill="#89d4ff" opacity="0.7"/>
      <rect x="404" y="220" width="126" height="12" rx="6" fill="#89d4ff" opacity="0.5"/>
      <text x="488" y="250" text-anchor="middle" font-size="14" fill="#dfeeff">Secure REST API • Azure deployment</text>

      <rect x="680" y="90" width="240" height="110" rx="16" fill="#1e2d3f" stroke="#ffcc6a" stroke-width="2" filter="url(#shadow)"/>
      <text x="800" y="122" text-anchor="middle" font-size="22" font-weight="700" fill="#fff4d6">Operations Console</text>
      <text x="800" y="150" text-anchor="middle" font-size="15" fill="#f8d995">Health / drift / compliance</text>
      <rect x="726" y="165" width="148" height="12" rx="6" fill="url(#cpp)"/>

      <g>
        <path d="M300 138 H358" stroke="#6ad1ff" stroke-width="4" stroke-linecap="round"/>
        <path d="M618 138 H680" stroke="#6ad1ff" stroke-width="4" stroke-linecap="round"/>
        <path d="M488 250 V320" stroke="#8ddcff" stroke-width="4" stroke-linecap="round"/>
      </g>

      <g>
        <rect x="118" y="286" width="220" height="92" rx="16" fill="#0a1d2e" stroke="#48a4ff" stroke-width="2" filter="url(#shadow)"/>
        <text x="228" y="320" text-anchor="middle" font-size="20" font-weight="700" fill="#dff5ff">On-prem Network</text>
        <text x="228" y="346" text-anchor="middle" font-size="14" fill="#96d6ff">Switches • Routers • Devices</text>
        <g transform="translate(160 355)">
          <rect x="0" y="0" width="26" height="16" rx="4" fill="#78d3ff"/>
          <rect x="36" y="0" width="26" height="16" rx="4" fill="#78d3ff"/>
          <rect x="72" y="0" width="26" height="16" rx="4" fill="#78d3ff"/>
        </g>
      </g>

      <g>
        <rect x="412" y="286" width="220" height="92" rx="16" fill="#0d2236" stroke="#f6b86a" stroke-width="2" filter="url(#shadow)"/>
        <text x="522" y="320" text-anchor="middle" font-size="20" font-weight="700" fill="#fff0cf">C++ Scanner</text>
        <text x="522" y="346" text-anchor="middle" font-size="14" fill="#f5d08c">Host-side discovery & checks</text>
        <g transform="translate(468 360)">
          <rect x="0" y="0" width="18" height="8" rx="2" fill="#ffbf69"/>
          <rect x="22" y="0" width="18" height="8" rx="2" fill="#ffbf69"/>
          <rect x="44" y="0" width="18" height="8" rx="2" fill="#ffbf69"/>
        </g>
      </g>

      <g>
        <path d="M338 332 H412" stroke="#f6b86a" stroke-width="4" stroke-linecap="round"/>
        <path d="M632 332 H680" stroke="#7ee0ff" stroke-width="4" stroke-linecap="round"/>
      </g>

      <g transform="translate(710 270)">
        <rect x="0" y="0" width="220" height="54" rx="12" fill="#0e1f36" stroke="#6fe1ff" stroke-width="2"/>
        <text x="110" y="23" text-anchor="middle" font-size="16" font-weight="700" fill="#e8f7ff">Cisco Packet Tracer</text>
        <text x="110" y="40" text-anchor="middle" font-size="11" fill="#9ae2ff">network lab / simulation</text>
        <circle cx="34" cy="27" r="10" fill="#0ea5e9"/>
        <path d="M29 27 L34 21 L39 27 L34 33 Z" fill="#dff6ff"/>
      </g>
    </g>
  </svg>
</div>

## Features

- Live device data collection from Cisco Meraki
- Automated health and compliance evaluation across distributed sites
- Secure FastAPI-based REST endpoints for operational visibility
- Azure-ready deployment for enterprise hosting
- Lightweight C++ agent for on-prem scanning and local data collection
- Hybrid network monitoring for modern enterprise environments

## Use Cases

- Network health tracking across branch and campus environments
- Compliance validation against internal operational standards
- Automated detection of outage risk, drift, and configuration mismatch
- Centralized visibility for network operations teams

## Tech Stack

- Python
- FastAPI
- Cisco Meraki API
- Azure
- C++
- RESTful service architecture

## Getting Started

1. Configure Meraki API credentials and Azure environment settings.
2. Deploy the FastAPI backend in Azure.
3. Run the C++ scan tool on the on-prem network side.
4. Query the API for device health, compliance status, and network insights.

## License

This project is intended for internal network automation and operation workflows. Update license terms to match your organization's policy before production use.

---

Built for modern enterprise network operations.
