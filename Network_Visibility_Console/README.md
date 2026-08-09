# Network Visibility Console

A FastAPI backend that connects to Cisco IOS switches using Netmiko and collects basic network information.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
cd backend
fastapi dev api.py
```

The API runs at `http://127.0.0.1:8000`.

API documentation is available at `http://127.0.0.1:8000/docs`.

## Current Features

- IPv4 address validation
- Username and password length validation
- Netmiko SSH connection to Cisco IOS devices
- Seed switch hostname collection
- ARP table collection
- Routing table collection
- Structured API responses for:
  - successful collection
  - authentication failure
  - connection timeout

## Endpoints

### Health check

```http
GET /health
```

### Switch snapshot

```http
POST /switch_snapshots
```

Example request:

```json
{
  "ip_address": "192.168.1.10",
  "username": "admin",
  "password": "password"
}
```

The endpoint returns success, authentication-failure, or connection-timeout information.

## Scope

This project is currently intended for use with Cisco devices in a local CML lab environment.