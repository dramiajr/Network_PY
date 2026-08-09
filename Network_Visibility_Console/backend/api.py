from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend_switch_side_logic import validate_ip, validate_passed_credentials, seed_switch_snapshot

"""
cd /path/to/backend
source .venv/bin/activate
fastapi dev api.py

deactivate 
"""   

app = FastAPI()

class Frontend_Request_Fields(BaseModel):
    ip_address: str
    username: str
    password: str

@app.get("/health")
def check_api_health():
    status = {
        "status" : "ok"
    }
    return status

@app.post("/switch_snapshots")
def run_initial_switch_side_request(request: Frontend_Request_Fields):
    # Pre Netmiko attempt validation
    valid_ip = validate_ip(request.ip_address)
    if not valid_ip:
        invalid_ip_address = {
            "status" : "failed",
            "message" : "Invalid IP Address"
        }
        return JSONResponse(status_code=400, content=invalid_ip_address)

    valid_credentials = validate_passed_credentials(request.username, request.password)
    if not valid_credentials:
        invalid_credentials = {
            "status" : "failed",
            "message" : "Username or Password must not exceed 25 characters"
        }
        return JSONResponse(status_code=400, content=invalid_credentials)

    # Initial Snapshot 
    seed_switch_ssh_attempt = seed_switch_snapshot(request.ip_address, request.username, request.password)

    format_frontend_response = seed_switch_ssh_attempt.get("result_type")

    if format_frontend_response == "success":
        initial_netmiko_snapshot = {
            "request_status": seed_switch_ssh_attempt["attempt_status"],
            "result_type" : seed_switch_ssh_attempt["result_type"],
            "device" : seed_switch_ssh_attempt["device"],
            "message" : seed_switch_ssh_attempt["message"]
        }   
        return JSONResponse(status_code=200, content=initial_netmiko_snapshot)
    
    elif format_frontend_response == "authentication_failure":
        initial_netmiko_snapshot = {
            "request_status": seed_switch_ssh_attempt["attempt_status"],
            "result_type" : seed_switch_ssh_attempt["result_type"],
            "device" : seed_switch_ssh_attempt["device"],
            "message" : seed_switch_ssh_attempt["message"]
        }
        return JSONResponse(status_code=502, content=initial_netmiko_snapshot)
    
    elif format_frontend_response == "connection_timeout":
        initial_netmiko_snapshot = {
            "request_status": seed_switch_ssh_attempt["attempt_status"],
            "result_type" : seed_switch_ssh_attempt["result_type"],
            "device" : seed_switch_ssh_attempt["device"],
            "message" : seed_switch_ssh_attempt["message"]
        }
        return JSONResponse(status_code=504, content=initial_netmiko_snapshot)
    
    else:
        fallback_response = {
            "request_status": "failed",
            "result_type": "unexpected_backend_result",
            "message": "An unexpected switch-side processing error occurred"
        }
        return JSONResponse(status_code=500, content=fallback_response)
    




