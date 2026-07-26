from fastapi import FastAPI
from initial_sw_troubleshooting import validate_ip, ping_target_ip

"""
cd /path/to/backend
source .venv/bin/activate
fastapi dev api.py

deactivate 
"""     

app = FastAPI()

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



    
