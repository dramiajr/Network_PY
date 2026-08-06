# Initial Troubleshooting Report

A small network troubleshooting prototype built with React and FastAPI. It runs ping and Cisco IOS interface checks, then displays the raw results in a browser.

This prototype is no longer under active development as the project is moving in a new direction.

## Screenshots

### Successful report

![Successful troubleshooting report](frontend/screenshots/linkedin-final/01-success-report-final.png)

### Running checks

![Running checks with cancel option](frontend/screenshots/linkedin-final/02-running-cancel-final.png)

### Authentication failure

![Authentication failure response](frontend/screenshots/linkedin-final/03-authentication-error-final.png)

## Built With

- React and Vite
- FastAPI
- Netmiko
- Python `ping`

## Run Locally

Start the backend:

```bash
cd backend
source .venv/bin/activate
fastapi dev api.py
```

Start the frontend in another terminal:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open `http://localhost:5173`.
