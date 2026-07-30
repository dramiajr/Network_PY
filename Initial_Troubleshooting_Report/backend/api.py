from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from initial_sw_troubleshooting import validate_ip, ping_target_ip

"""
cd /path/to/backend
source .venv/bin/activate
fastapi dev api.py

deactivate 
"""     

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    status = {
        "update": "working"
    }
    return status 

@app.get("/ping")
def run_ping(ip_address: str):
    valid_ip = validate_ip(ip_address)
    if valid_ip == False:
        invalid_ip = {
            "request_status": "invalid",
            "message": "Invalid IP Address",
            "invalid_address": ip_address
        }
        return invalid_ip
    else:
        ping_attempt = ping_target_ip(ip_address)
        return ping_attempt

@app.get("/switch-side")
def run_switchside_logic():

    return

    
