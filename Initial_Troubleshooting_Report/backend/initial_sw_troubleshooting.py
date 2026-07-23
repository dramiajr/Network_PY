import subprocess

# IP Validation Logic 
def validate_ip(ip_address):
    split_ip = ip_address.split(".")
    if len(split_ip) == 4:
        for octet in split_ip:
            if octet == "":
                return False
            elif len(octet) > 3:
                return False
            elif not octet.isdigit():
                return False
            elif len(octet) > 1 and octet[0] == "0":
                return False
            else:
                converted_octet = int(octet)
                if not 0 <= converted_octet <= 255:
                    return False
        return True
    else:
        return False

# Prompt for IP loop
def get_target_ip():
    ip_address = input("Enter IP: ")
    valid_ip = validate_ip(ip_address)
    while not valid_ip:
        ip_address = input("Enter a valid IP Address: ")
        valid_ip = validate_ip(ip_address)
    return ip_address

# Ping Command, Attempt, & Storing Logic
def ping_target_ip(ip_address):

    # Use for Linux 
    ping_command = ["ping", "-4", "-c", "4", ip_address]
    
    # Use for Windows
    #ping_command = ["ping", "-4", "-n", "4", ip_address]
    ping_attempt = subprocess.run(
        ping_command,
        capture_output=True,
        text=True
    )
    ping_output = ping_attempt.stdout
    ping_outcome = ping_attempt.returncode
    if ping_outcome == 2:
        ping_status = "error"
    elif ping_outcome == 1:
        ping_status = "no reply"
    else:
        ping_status ="successful"
        

    stored_ping_result = {
        "ping_status": ping_status,
        "ping_output_raw": ping_output 
    }
    return stored_ping_result



def main():
    target_ip = get_target_ip()

    stored_ping_result = ping_target_ip(target_ip)

    print("\nICMP Checks")
    print("Status:", stored_ping_result["ping_status"])
    print(stored_ping_result["ping_output_raw"])

if __name__ == "__main__":
    main()
