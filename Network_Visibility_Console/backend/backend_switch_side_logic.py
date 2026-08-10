from netmiko import ConnectHandler 
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

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

def validate_passed_credentials(username, password):
    if len(username) <= 25 and len(password) <= 25:
        return True
    else:
        return False

def netmiko_device_information(ip_address, username, password):
    netmiko_device_info = {
        "device_type" : "cisco_ios",
        "host" : ip_address,
        "username" : username,
        "password": password
    }
    return netmiko_device_info

def seed_switch_snapshot(ip_address, username, password):
    standardized_netmiko_information = netmiko_device_information(ip_address, username, password)

    run_netmiko = None

    try:

        run_netmiko = ConnectHandler(**standardized_netmiko_information)

        get_seed_sw_hostname = run_netmiko.send_command("show version | include uptime is")
        seed_sw_hostname = get_seed_sw_hostname.split()[0]

        get_seed_sw_arp_table = run_netmiko.send_command("show ip arp")

        get_seed_sw_route_table = run_netmiko.send_command("show ip route | include ^[A-Za-z*+%].*[0-9]/[0-9]")

        get_seed_sw_cdp_neighbors_detail = run_netmiko.send_command("show cdp neighbors detail | include Device|IP|Interface|Duplex")
        seed_cdp_neighbors_detail_raw = get_seed_sw_cdp_neighbors_detail.strip().split("Device ID:")



        initial_sw_snapshot = {
            "result_type" : "success",
            "attempt_status" : "success",
            "device" : f"{ip_address}:22",
            "message" : "Seed Switch Snapshot",
            "hostname" : seed_sw_hostname,
            "raw_arp_table" : get_seed_sw_arp_table,
            "filtered_route_table" : get_seed_sw_route_table,
        }
        
    except NetmikoAuthenticationException:
        authentication_failure = {
            "result_type" : "authentication_failure",
            "attempt_status" : "failed",
            "message" : "Authentication to device failed",
            "device" : f"{ip_address}:22"
        }
        return authentication_failure
    
    except NetmikoTimeoutException:
        connection_timeout = {
            "result_type" : "connection_timeout",
            "attempt_status" : "failed",
            "message" : "Connection attempt timed out",
            "device" : f"{ip_address}:22"
        }
        return connection_timeout

    finally:
        if run_netmiko is not None:
            run_netmiko.disconnect()

    return initial_sw_snapshot   


def main():
    x = "172.16.100.10"
    y = "ts_app"
    z = "troubleShooting!"

    std_format = netmiko_device_information(x,y,z)

    netmiko_cmd = ConnectHandler(**std_format)
    cdp_neighbors = netmiko_cmd.send_command("show cdp neighbors detail | include Device|IP|Interface|Duplex")

    neighbors_detail_raw = cdp_neighbors.split("Device")

    for unique_block in neighbors_detail_raw:
        if unique_block == "":
            continue
        else:
            cdp_neighbor = unique_block
            print(cdp_neighbor)

"""
    print(neighbors_detail_raw[1])
    print("\n")
    print(neighbors_detail_raw[2])

    parsed = neighbors_detail_raw[1].split("\n")
    print(parsed[0].strip())
    print(parsed[1].strip())
    parsed_int = parsed[2].split(",")
    print(parsed_int[0])
    print(parsed_int[1].strip())
    print(parsed[3])

    parsed2 = neighbors_detail_raw[2].split("\n")
    print(parsed2[0].strip())
    print(parsed2[1].strip())
    parsed2_int = parsed2[2].split(",")
    print(parsed2_int[0])
    print(parsed2_int[1].strip())
    print(parsed2[3])

"""
    

    




if __name__ == "__main__":
    main()