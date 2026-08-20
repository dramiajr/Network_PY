from dotenv import load_dotenv
import os
from netmiko import ConnectHandler 
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

load_dotenv()

def validate_ip(ip_address):
    octet_strings = ip_address.split(".")
    if len(octet_strings) == 4:
        for octet in octet_strings:
            if octet == "":
                return False
            elif len(octet) > 3:
                return False
            elif not octet.isdigit():
                return False
            elif len(octet) > 1 and octet[0] == "0":
                return False
            else:
                octet_value = int(octet)
                if not 0 <= octet_value <= 255:
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
    netmiko_params = {
        "device_type" : "cisco_ios",
        "host" : ip_address,
        "username" : username,
        "password": password
    }
    return netmiko_params

def seed_switch_snapshot(ip_address, username, password):
    netmiko_params = netmiko_device_information(ip_address, username, password)

    connection = None

    try:
        connection = ConnectHandler(**netmiko_params)

        # Collect the seed-switch data included in the initial API response.
        show_version_output = connection.send_command("show version | include uptime is")
        hostname = show_version_output.split()[0]

        arp_table_output = connection.send_command("show ip arp")

        route_table_output = connection.send_command("show ip route | include ^[A-Za-z*+%].*[0-9]/[0-9]")

        snapshot = {
            "result_type" : "success",
            "attempt_status" : "success",
            "device" : f"{ip_address}:22",
            "message" : "Seed Switch Snapshot",
            "hostname" : hostname,
            "raw_arp_table" : arp_table_output,
            "filtered_route_table" : route_table_output
        }

        # Filter CDP output on the device to reduce the data transferred and parsed.
        cdp_output = connection.send_command("show cdp neighbors detail | include Device|IP|Interface|Duplex|Total")

        cdp_summary = {}

        cdp_lines = cdp_output.strip().split("\n")

        # Cisco IOS reports the neighbor count in a trailing "Total cdp entries" line.
        for line in cdp_lines:
            if "Total cdp entries" in line:
                neighbor_count_fields = line.strip().split(":")
                neighbor_count = int(neighbor_count_fields[1])
                cdp_summary["total_cdp_entries"] = neighbor_count

        # Each CDP record begins with "Device ID:", so "Device" separates records.
        neighbor_blocks = cdp_output.strip().split("Device")

        neighbors = []

        for neighbor_block in neighbor_blocks:
            if neighbor_block == "":
                continue

            neighbor = {}

            neighbor_lines = neighbor_block.strip().split("\n")

            # Retain only the fields needed for topology discovery.
            for line in neighbor_lines:
                if "ID:" in line:
                    hostname_parts = line.split(":")
                    neighbor["cdp_neighbor_hostname"] = hostname_parts[1].strip()

                elif "IP address:" in line:
                    ip_address_parts = line.split(":")
                    neighbor["cdp_neighbor_ip_address"] = ip_address_parts[1].strip()

                elif "Interface:" in line:
                    interface_parts = line.split(":")
                    local_interface_parts = interface_parts[1].split(",")
                    neighbor["local_interface"] = local_interface_parts[0].strip()
                    neighbor["outgoing_interface"] = interface_parts[2].strip()

                elif "Duplex" in line:
                    duplex_parts = line.split(":")
                    neighbor["duplex"] = duplex_parts[1].strip()

            if line:
                neighbors.append(neighbor)

            # Collect interface and route evidence for each discovered neighbor.
            for discovered_neighbor in neighbors:
                evidence = {}

                if "local_interface" in discovered_neighbor:
                    local_interface = discovered_neighbor["local_interface"].strip()
                    interface_output = connection.send_command(f"show interfaces {local_interface}")
                    evidence["local_int_output"] = interface_output.strip()

                if "cdp_neighbor_ip_address" in discovered_neighbor:
                    neighbor_ip_address = discovered_neighbor["cdp_neighbor_ip_address"]
                    route_output = connection.send_command(f"show ip route {neighbor_ip_address}")
                    evidence["cdp_neighbor_route"] = route_output.strip()

                    cef_output = connection.send_command(f"show ip cef {neighbor_ip_address}")
                    evidence["cef"] = cef_output.strip()

            

            if discovered_neighbor:
                neighbor["evidence"] = evidence

        cdp_summary["cdp_neighbors"] = neighbors

        snapshot["cdp_neighbors"] = cdp_summary
        
    except NetmikoAuthenticationException:
        authentication_failure_result = {
            "result_type" : "authentication_failure",
            "attempt_status" : "failed",
            "message" : "Authentication to device failed",
            "device" : f"{ip_address}:22"
        }
        return authentication_failure_result
    
    except NetmikoTimeoutException:
        connection_timeout_result = {
            "result_type" : "connection_timeout",
            "attempt_status" : "failed",
            "message" : "Connection attempt timed out",
            "device" : f"{ip_address}:22"
        }
        return connection_timeout_result

    finally:
        if connection is not None:
            connection.disconnect()

    return snapshot   

def main():
    x = os.getenv("LAB_SWITCH_IP")
    y = os.getenv("LAB_SWITCH_USER")
    z = os.getenv("LAB_SWITCH_PWD")

    #result = seed_switch_snapshot(x, y, z)
    #print(result)

    std_format = netmiko_device_information(x,y,z)

    netmiko_cmd = ConnectHandler(**std_format)
    cdp_neighbors = netmiko_cmd.send_command("show cdp neighbors detail | include Device|IP|Interface|Duplex|Total")

    cdp_results = {}

    find_cdp_entries = cdp_neighbors.split("\n")

    for cdp_entries in find_cdp_entries:
        if "Total cdp entries" in cdp_entries:
            extract_cdp_entries = cdp_entries.split(":")
            extracted_cdp_entries = int(extract_cdp_entries[1].strip())
            cdp_results["cdp_entries"] = extracted_cdp_entries

    cdp_neighbors_list = []

    neighbors_detail_array = cdp_neighbors.split("Device")

    for neighbors in neighbors_detail_array:
        if neighbors == "":
            continue

        current_neighbor = {}

        split_unique_neighbors = neighbors.strip().split("\n")

        for unique_neighbor in split_unique_neighbors:
            if "ID:" in unique_neighbor:
                extract_hostname = unique_neighbor.split(":")
                current_neighbor["cdp_neighbor_hostname"] = extract_hostname[1].strip()

            elif "IP address:" in unique_neighbor:
                extract_ip_address = unique_neighbor.split(":")
                current_neighbor["cdp_neighbor_ip_address"] = extract_ip_address[1].strip()

            elif "Interface:" in unique_neighbor:
                extract_interfaces = unique_neighbor.split(":")
                extract_local_interfaces = extract_interfaces[1].split(",")
                current_neighbor["local_interface"] = extract_local_interfaces[0].strip()
                current_neighbor["outgoing_interface"] = extract_interfaces[2].strip()

            elif "Duplex" in unique_neighbor:
                extract_duplex = unique_neighbor.split(":")
                current_neighbor["duplex"] = extract_duplex[1].strip()

        if current_neighbor:
            cdp_neighbors_list.append(current_neighbor)

        for loop in cdp_neighbors_list:
            cdp_neighbor_additional_command_results = {}

            if "local_interface" in loop:
                local_interface = loop["local_interface"].strip()
                check_local_interface = netmiko_cmd.send_command(f"show interfaces {local_interface}")
                cdp_neighbor_additional_command_results["local_interface_check"] = check_local_interface.strip()

            if "cdp_neighbor_ip_address" in loop:
                neighbor_ip = loop["cdp_neighbor_ip_address"]
                check_route_to_neighbor = netmiko_cmd.send_command(f"show ip route {neighbor_ip}")
                cdp_neighbor_additional_command_results["cdp_neighbor_route"] = check_route_to_neighbor.strip()

        if loop:
            current_neighbor["evidence"] = cdp_neighbor_additional_command_results

    #print(f"{cdp_neighbors_list}")


if __name__ == "__main__":
    main()
