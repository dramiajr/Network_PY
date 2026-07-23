from fastapi import FastAPI
from initial_sw_troubleshooting import validate_ip, ping_target_ip
# to run locally: "fastapi dev api.py"     

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
        return valid_ip
    else:
        ping_attempt = ping_target_ip(ip_address)
        return ping_attempt



    
