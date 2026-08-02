from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from initial_sw_troubleshooting import validate_ip, ping_target_ip, validate_interface_type, validate_interface_number, netmiko_operations

"""
cd /path/to/backend
source .venv/bin/activate
fastapi dev api.py

deactivate 
"""     

class Frontend_Request_Fields(BaseModel):
    ip_address: str
    interface_type: str
    interface_number: str
    username: str
    password: str

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
    
    ping_attempt = ping_target_ip(ip_address)
    return ping_attempt
    
@app.post("/switch-side")
def run_switchside_logic(request: Frontend_Request_Fields):

    valid_ip = validate_ip(request.ip_address)

    if valid_ip == False:
        invalid_ip = {
            "request_status": "invalid",
            "message": "Invalid IP Address",
            "invalid_address": request.ip_address
        }
        return invalid_ip
    
    valid_int_type = validate_interface_type(request.interface_type)
    valid_int_number = validate_interface_number(request.interface_number)

    if valid_int_type == False or valid_int_number == False:
        invalid_interface = {
            "invalid_interface" : f"{request.interface_type}{request.interface_number}"
        }
        return invalid_interface

    interface = request.interface_type + request.interface_number
    switchside_results = netmiko_operations(request.ip_address, interface, request.username, request.password)

    backend_response = {
        "switch_results" : switchside_results
    }
    
    return backend_response

    
