# Initial Troubleshooting Tool

## What It Is

Initial Troubleshooting Tool is a local-first network troubleshooting project. It runs approved checks on the local machine, preserves raw evidence, and displays structured results without diagnosing root cause.

## Current Status

The current working MVP supports:

- React/Vite frontend
- FastAPI backend
- Target IPv4 input
- Local ping execution
- Valid and invalid input handling
- Loading, request errors, and a five-second request timeout
- Display of ping status and raw ping output

Traceroute, simulated device commands, full report sections, Docker packaging, and production deployment are not complete yet.

## Project Structure

```text
.
├── backend/
│   ├── api.py
│   └── initial_sw_troubleshooting.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Local Development

The current local Python environment is located at `backend/.venv`. From the project root, start the backend:

```bash
cd backend
source .venv/bin/activate
fastapi dev api.py
```

In a second terminal, from the project root, start the frontend:

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in a browser. Vite may print a different URL if that port is unavailable.

To stop both servers, press `Ctrl+C` in the FastAPI terminal and in the Vite terminal. After FastAPI stops, leave the Python virtual environment:

```bash
deactivate
```

Recreating the Python environment needs confirmation because the repository does not currently include a Python dependency manifest.

## Current Request Flow

```text
React form
→ FastAPI /ping endpoint
→ Python ping function
→ structured JSON
→ frontend report
```

## Next Steps

- Extract React components
- Move the API URL into environment configuration
- Add traceroute status and raw evidence
- Add simulated device-output workflows
- Add Docker Compose later
