from flask import Flask
import meraki

app = Flask(__name__)

API_KEY = "977b24744ba4fbe1bff8c6bd048b632bd692d967"
ORG_ID = "1795064"

dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)


def fetch_networks():
    """Real Meraki data — falls back to mock data if the API call fails or is empty."""
    try:
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


def check_network_health(network):
    """Simple compliance logic: flag any network that's offline."""
    if network.get("status") == "offline":
        return {"healthy": False, "issue": f"Network '{network['name']}' is offline"}
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

    result = check_network_health(network)
    return {"network_id": network_id, "name": network["name"], **result}


if __name__ == '__main__':
    app.run(debug=True)