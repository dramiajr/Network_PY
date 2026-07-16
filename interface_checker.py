interface_evidence = {
    "interface": "GigabitEthernet0/1",
    "admin_up": False,
    "oper_up": True,
    "recent_flaps": 2,
}


def historical_instability(interface):
    return interface["recent_flaps"] > 0


def current_state_healthy(interface):
    return interface["admin_up"] and interface["oper_up"]

def classify_current_state(interface):
    if not interface["admin_up"] and not interface["oper_up"]:
        return "administratively_down"
    elif interface["admin_up"] and not interface["oper_up"]:
        return "physically_down"
    elif interface["admin_up"] and interface["oper_up"]:
        return "up"
    else:
        return "ambiguous_state"

#print("Interface:", 
#    classify_current_state(interface_evidence))

print(
    f"{interface_evidence['interface']}: "
    f"{classify_current_state(interface_evidence)}, "
    f"historical instability = "
    f"{historical_instability(interface_evidence)}"
)