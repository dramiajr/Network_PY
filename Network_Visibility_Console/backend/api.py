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
    # Reject invalid input before opening an SSH connection.
    is_ip_valid = validate_ip(request.ip_address)
    if not is_ip_valid:
        error_payload = {
            "status" : "failed",
            "message" : "Invalid IP Address"
        }
        return JSONResponse(status_code=400, content=error_payload)

    credential_lengths_are_valid = validate_passed_credentials(request.username, request.password)
    if not credential_lengths_are_valid:
        error_payload = {
            "status" : "failed",
            "message" : "Username or Password must not exceed 25 characters"
        }
        return JSONResponse(status_code=400, content=error_payload)

    # Collect the initial snapshot from the seed switch.
    snapshot_result = seed_switch_snapshot(request.ip_address, request.username, request.password)

    result_type = snapshot_result.get("result_type")

    if result_type == "success":
        response_payload = {
            "request_status": snapshot_result["attempt_status"],
            "result_type" : snapshot_result["result_type"],
            "device" : snapshot_result["device"],
            "message" : snapshot_result["message"],
            "seed_sw_hostname": snapshot_result["hostname"],
            "seed_sw_arp_table": snapshot_result["raw_arp_table"],
            "seed_sw_filtered_route_table" : snapshot_result["filtered_route_table"],
            "seed_sw_cdp_neighbors_list" : snapshot_result["cdp_neighbors"]
        }   
        return JSONResponse(status_code=200, content=response_payload)
    
    elif result_type == "authentication_failure":
        response_payload = {
            "request_status": snapshot_result["attempt_status"],
            "result_type" : snapshot_result["result_type"],
            "device" : snapshot_result["device"],
            "message" : snapshot_result["message"]
        }
        return JSONResponse(status_code=502, content=response_payload)
    
    elif result_type == "connection_timeout":
        response_payload = {
            "request_status": snapshot_result["attempt_status"],
            "result_type" : snapshot_result["result_type"],
            "device" : snapshot_result["device"],
            "message" : snapshot_result["message"]
        }
        return JSONResponse(status_code=504, content=response_payload)
    
    else:
        error_payload = {
            "request_status": "failed",
            "result_type": "unexpected_backend_result",
            "message": "An unexpected switch-side processing error occurred"
        }
        return JSONResponse(status_code=500, content=error_payload)
    


