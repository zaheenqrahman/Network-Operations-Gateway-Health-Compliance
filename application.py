import os
from flask import Flask
import meraki

app = Flask(__name__)

API_KEY = os.environ.get("MERAKI_API_KEY", "")
ORG_ID = os.environ.get("ORG_ID", "")

try:
    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
except Exception as e:
    print(f"Meraki client init failed, will use mock data: {e}")
    dashboard = None


def fetch_networks():
    """Real Meraki data — falls back to mock data if the API call fails or is empty."""
    try:
        if dashboard is None:
            raise RuntimeError("Meraki client not initialized")
        real_data = dashboard.organizations.getOrganizationNetworks(ORG_ID)
        if real_data:
            return real_data
    except Exception as e:
        print(f"Meraki call failed, using mock data: {e}")

    return [
        {"id": "N_1001", "name": "Main Office", "status": "online", "type": "wireless"},
        {"id": "N_1002", "name": "Branch Office - East", "status": "offline", "type": "wired"},
        {"id": "N_1003", "name": "Data Center VLAN", "status": "online", "type": "vlan"},
    ]


def fetch_devices():
    """Real Meraki device data — falls back to mock data if the API call fails or is empty."""
    try:
        if dashboard is None:
            raise RuntimeError("Meraki client not initialized")
        real_data = dashboard.organizations.getOrganizationDevices(ORG_ID)
        if real_data:
            return real_data
    except Exception as e:
        print(f"Meraki call failed, using mock data: {e}")

    return [
        {"serial": "Q2XX-XXXX-0001", "name": "Main-AP-1", "model": "MR20", "status": "online"},
        {"serial": "Q2XX-XXXX-0002", "name": "Main-Firewall", "model": "MX100", "status": "online"},
        {"serial": "Q2XX-XXXX-0003", "name": "Branch-Switch", "model": "MS250-24", "status": "offline"},
    ]


def fetch_device_statuses():
    """Live per-device status (online/offline/alerting/dormant) — separate from
    fetch_devices()'s static info, since getOrganizationDevices doesn't include it."""
    try:
        if dashboard is None:
            raise RuntimeError("Meraki client not initialized")
        real_data = dashboard.organizations.getOrganizationDevicesStatuses(ORG_ID)
        if real_data:
            return real_data
    except Exception as e:
        print(f"Meraki call failed, using mock statuses: {e}")

    return [
        {"serial": "Q2XX-XXXX-0001", "networkId": "N_1001", "status": "online"},
        {"serial": "Q2XX-XXXX-0002", "networkId": "N_1001", "status": "online"},
        {"serial": "Q2XX-XXXX-0003", "networkId": "N_1002", "status": "offline"},
    ]


def check_network_health(network, device_statuses):
    """A network is unhealthy if any of its devices are offline or alerting."""
    bad = {"offline", "alerting"}
    down = [d for d in device_statuses if d.get("networkId") == network["id"] and d.get("status") in bad]
    if down:
        names = ", ".join(d.get("name") or d.get("serial", "unknown device") for d in down)
        return {"healthy": False, "issue": f"Network '{network['name']}' has device(s) down: {names}"}
    return {"healthy": True, "issue": None}


@app.route('/')
def index():
    return 'Hello!'


@app.route('/networks')
def get_networks():
    return {"networks": fetch_networks()}


@app.route('/devices')
def get_devices():
    return {"devices": fetch_devices()}


@app.route('/networks/<network_id>/health')
def get_network_health(network_id):
    networks = fetch_networks()
    network = next((n for n in networks if n["id"] == network_id), None)

    if network is None:
        return {"error": f"Network '{network_id}' not found"}, 404

    device_statuses = fetch_device_statuses()
    result = check_network_health(network, device_statuses)
    return {"network_id": network_id, "name": network["name"], **result}

def check_device_compliance(device, device_statuses):
    " ff device against single compliance rule set, like if its on the approved list/offline,etc"
    issues = []
    # 1: Flags if device is offline (live status, looked up by serial)
    status = next((s.get("status") for s in device_statuses if s.get("serial") == device.get("serial")), None)
    if status == "offline":
        issues.append("Device is offline")

    # 2: flag if statement if device is not an approved model
    approved_models = ["MR20", "MX100", "MS250-24"]
    if device.get("model") not in approved_models:
        issues.append(f"Model {device.get('model')} is not on the approved list")

    # returns basically an else statement of the compliance and issues found
    return{
        "compliant" : len(issues) == 0,
        "issues": issues
    }

@app.route('/devices/<serial>/compliance')
def get_device_compliance(serial):
    devices = fetch_devices()
    device = next((d for d in devices if d ["serial"] == serial), None)

    if device is None:
        return {"error": f"Device '{serial}' not found"}, 404

    device_statuses = fetch_device_statuses()
    result = check_device_compliance(device, device_statuses)
    return {"serial": serial, "name": device["name"], **result}
# should print it out the ohome address weblink but adjust it with the compliance and devices url added

@app.route('/alerts/scan', methods = ['POST'])
def scan_alerts():
    networks = fetch_networks()
    device_statuses = fetch_device_statuses()
    alerts = []

    for network in networks:
        result = check_network_health(network, device_statuses)
        if result["healthy"] == False:
            alerts.append(result["issue"])

    return{"alerts_found": len(alerts), "alerts": alerts}

if __name__ == '__main__':
    app.run(debug=True)