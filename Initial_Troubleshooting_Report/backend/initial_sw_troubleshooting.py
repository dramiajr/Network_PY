import subprocess
import getpass
from netmiko import ConnectHandler 

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

# Interface Type Validation Logic
def validate_interface_type(interface_type):
    approved_int_type = ["Fa", "Gi", "Te"]
    if interface_type not in approved_int_type:
        return False
    else:
        return True

# Interface Nummber Validation Logic
def validate_interface_number(interface_number):
    split_int = interface_number.split("/")

    if len(split_int) == 2 or len(split_int) == 3:
        for section in split_int:
            if section == "":
                return False
            elif len(section) > 3:
                return False
            elif not section.isdigit():
                return False
        return True
    else:
        return False

# Get Interface from User
def get_interface():
    interface_type = input("Enter Interface Type (Fa, Gi, Te): ")
    valid_int_type = validate_interface_type(interface_type)
    while valid_int_type == False:
        interface_type = input("Enter Interface Type (Fa, Gi, Te): ")
        valid_int_type = validate_interface_type(interface_type)
    
    interface_number = input("Enter Interface: ")
    valid_int_num = validate_interface_number(interface_number)
    while valid_int_num == False:
        interface_number = input("Enter Interface: ")
        valid_int_num = validate_interface_number(interface_number)

    valid_interface = interface_type + interface_number

    return valid_interface


def get_ssh_credentials():
    username = input("Enter Username: ")
    while username == "":
        username = input("Enter Username: ")

    password = getpass.getpass("Enter Password: ", echo_char="*")
    while password == "":
        password = getpass.getpass("Enter Password: ", echo_char="*")

    ssh_credentials = {
        "username" : username,
        "password" : password
    }

    return(ssh_credentials)  

def netmiko_device_information(ip_address, username, password):
    device_info = {
        "device_type" : "cisco_ios",
        "host" : ip_address,
        "username" : username,
        "password": password
    }

    return device_info

def netmiko_operations(ip_address, interface, username, password):
    stored_device_information = netmiko_device_information(ip_address, username, password)

    net_connect = ConnectHandler(**stored_device_information)
    show_interfaces_target = net_connect.send_command(f"show interfaces {interface}")
    net_connect.disconnect()

def main():
    target_ip = get_target_ip()
    target_interface = get_interface()
    user_credentials = get_ssh_credentials()
    stored_device_information = netmiko_device_information(target_ip, user_credentials["username"], user_credentials["password"])
    stored_ping_result = ping_target_ip(target_ip)

    net_connect = ConnectHandler(**stored_device_information)
    show_interfaces_target = net_connect.send_command(f"show interfaces {target_interface}")

    print(f"\n{show_interfaces_target}")
    net_connect.disconnect()
#"""
    print("\nICMP Checks")
    print("Status:", stored_ping_result["ping_status"])
    print(stored_ping_result["ping_output_raw"])
#"""


if __name__ == "__main__":
    main()
