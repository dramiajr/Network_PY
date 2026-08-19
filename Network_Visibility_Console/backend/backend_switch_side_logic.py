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

        # Collect the seed-switch data included in the initial API response.
        get_seed_sw_hostname = run_netmiko.send_command("show version | include uptime is")
        seed_sw_hostname = get_seed_sw_hostname.split()[0]

        get_seed_sw_arp_table = run_netmiko.send_command("show ip arp")

        get_seed_sw_route_table = run_netmiko.send_command("show ip route | include ^[A-Za-z*+%].*[0-9]/[0-9]")

        initial_sw_snapshot = {
            "result_type" : "success",
            "attempt_status" : "success",
            "device" : f"{ip_address}:22",
            "message" : "Seed Switch Snapshot",
            "hostname" : seed_sw_hostname,
            "raw_arp_table" : get_seed_sw_arp_table,
            "filtered_route_table" : get_seed_sw_route_table
        }

        # Filter CDP output on the device to reduce the data transferred and parsed.
        get_seed_sw_cdp_neighbors_detail = run_netmiko.send_command("show cdp neighbors detail | include Device|IP|Interface|Duplex|Total")

        seed_sw_cdp_neighbor_results = {}

        seed_sw_cdp_neighbor_entries_raw = get_seed_sw_cdp_neighbors_detail.strip().split("\n")

        # Cisco IOS reports the neighbor count in a trailing "Total cdp entries" line.
        for cdp_entries in seed_sw_cdp_neighbor_entries_raw:
            if "Total cdp entries" in cdp_entries:
                parse_cdp_entries = cdp_entries.strip().split(":")
                cdp_entries_displayed = int(parse_cdp_entries[1])
                seed_sw_cdp_neighbor_results["total_cdp_entries"] = cdp_entries_displayed

        # Each CDP record begins with "Device ID:", so "Device" separates records.
        seed_sw_cdp_neighbors_detail_raw = get_seed_sw_cdp_neighbors_detail.strip().split("Device")

        seed_sw_cdp_neighbors_list = []

        for unique_entry in seed_sw_cdp_neighbors_detail_raw:
            if unique_entry == "":
                continue

            store_unique_cdp_neighbors = {}

            unique_entry_split = unique_entry.strip().split("\n")

            # Retain only the fields needed for topology discovery.
            for cdp_neighbor in unique_entry_split:
                if "ID:" in cdp_neighbor:
                    extract_hostname = cdp_neighbor.split(":")
                    store_unique_cdp_neighbors["cdp_neighbor_hostname"] = extract_hostname[1].strip()

                elif "IP address:" in cdp_neighbor:
                    extract_ip_address = cdp_neighbor.split(":")
                    store_unique_cdp_neighbors["cdp_neighbor_ip_address"] = extract_ip_address[1].strip()

                elif "Interface:" in cdp_neighbor:
                    extract_interfaces = cdp_neighbor.split(":")
                    extract_local_interfaces = extract_interfaces[1].split(",")
                    store_unique_cdp_neighbors["local_interface"] = extract_local_interfaces[0].strip()
                    store_unique_cdp_neighbors["outgoing_interface"] = extract_interfaces[2].strip()

                elif "Duplex" in cdp_neighbor:
                    extract_duplex = cdp_neighbor.split(":")
                    store_unique_cdp_neighbors["duplex"] = extract_duplex[1].strip()

            if cdp_neighbor:
                seed_sw_cdp_neighbors_list.append(store_unique_cdp_neighbors)

            # Collect interface and route evidence for each discovered neighbor.
            for loop_through in seed_sw_cdp_neighbors_list:
                cdp_neighbor_additional_command_results = {}

                if "local_interface" in loop_through:
                    local_interface = loop_through["local_interface"].strip()
                    check_local_interface = run_netmiko.send_command(f"show interfaces {local_interface}")
                    cdp_neighbor_additional_command_results["local_interface_check"] = check_local_interface.strip()

                if "cdp_neighbor_ip_address" in loop_through:
                    neighbor_ip = loop_through["cdp_neighbor_ip_address"]
                    check_route_to_neighbor = run_netmiko.send_command(f"show ip route {neighbor_ip}")
                    cdp_neighbor_additional_command_results["cdp_neighbor_route"] = check_route_to_neighbor.strip()

            if loop_through:
                store_unique_cdp_neighbors["evidence"] = cdp_neighbor_additional_command_results

        seed_sw_cdp_neighbor_results["cdp_neighbors"] = seed_sw_cdp_neighbors_list

        initial_sw_snapshot["cdp_neighbors"] = seed_sw_cdp_neighbor_results
        
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

    result = seed_switch_snapshot(x, y, z)
    print(result)

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

    print(f"{cdp_neighbors_list}")


if __name__ == "__main__":
    main()
