import hmac
import os
from datetime import datetime, timezone

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import meraki

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///netops.db")
db = SQLAlchemy(app)


class HealthCheck(db.Model):
    """One row per network per /alerts/scan run, so health can be reviewed over time."""
    id = db.Column(db.Integer, primary_key=True)
    checked_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    network_id = db.Column(db.String(64), nullable=False, index=True)
    network_name = db.Column(db.String(128), nullable=False)
    healthy = db.Column(db.Boolean, nullable=False)
    issue = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(8), nullable=False)  # "live" or "mock"

    def to_dict(self):
        return {
            "id": self.id,
            "checked_at": self.checked_at.isoformat(),
            "network_id": self.network_id,
            "network_name": self.network_name,
            "healthy": self.healthy,
            "issue": self.issue,
            "source": self.source,
        }


with app.app_context():
    db.create_all()


@app.before_request
def require_token():
    if request.path == "/":
        return None
    expected = os.environ.get("GATEWAY_TOKEN", "")
    supplied = request.headers.get("X-API-Token", "")
    if not expected:
        return jsonify(error="server auth not configured"), 503
    if not hmac.compare_digest(supplied, expected):
        return jsonify(error="unauthorized"), 401
    return None


API_KEY = os.environ.get("MERAKI_API_KEY", "")
ORG_ID = os.environ.get("ORG_ID", "")

try:
    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
except Exception as e:
    print(f"Meraki client init failed, will use mock data: {e}")
    dashboard = None


def fetch_networks():
    """Real Meraki data — falls back to mock data if the API call fails or is empty.
    Returns (data, source) where source is "live" or "mock", so callers/responses
    can be explicit about which one was used instead of silently mixing them."""
    try:
        if dashboard is None:
            raise RuntimeError("Meraki client not initialized")
        real_data = dashboard.organizations.getOrganizationNetworks(ORG_ID)
        if real_data:
            return real_data, "live"
    except Exception as e:
        print(f"Meraki call failed, using mock data: {e}")

    return [
        {"id": "N_1001", "name": "Main Office", "status": "online", "type": "wireless"},
        {"id": "N_1002", "name": "Branch Office - East", "status": "offline", "type": "wired"},
        {"id": "N_1003", "name": "Data Center VLAN", "status": "online", "type": "vlan"},
    ], "mock"


def fetch_devices():
    """Real Meraki device data — falls back to mock data if the API call fails or is empty.
    Returns (data, source) — see fetch_networks()."""
    try:
        if dashboard is None:
            raise RuntimeError("Meraki client not initialized")
        real_data = dashboard.organizations.getOrganizationDevices(ORG_ID)
        if real_data:
            return real_data, "live"
    except Exception as e:
        print(f"Meraki call failed, using mock data: {e}")

    return [
        {"serial": "Q2XX-XXXX-0001", "name": "Main-AP-1", "model": "MR20", "status": "online"},
        {"serial": "Q2XX-XXXX-0002", "name": "Main-Firewall", "model": "MX100", "status": "online"},
        {"serial": "Q2XX-XXXX-0003", "name": "Branch-Switch", "model": "MS250-24", "status": "offline"},
    ], "mock"


def fetch_device_statuses():
    """Live per-device status (online/offline/alerting/dormant) — separate from
    fetch_devices()'s static info, since getOrganizationDevices doesn't include it.
    Returns (data, source) — see fetch_networks()."""
    try:
        if dashboard is None:
            raise RuntimeError("Meraki client not initialized")
        real_data = dashboard.organizations.getOrganizationDevicesStatuses(ORG_ID)
        if real_data:
            return real_data, "live"
    except Exception as e:
        print(f"Meraki call failed, using mock statuses: {e}")

    return [
        {"serial": "Q2XX-XXXX-0001", "networkId": "N_1001", "status": "online"},
        {"serial": "Q2XX-XXXX-0002", "networkId": "N_1001", "status": "online"},
        {"serial": "Q2XX-XXXX-0003", "networkId": "N_1002", "status": "offline"},
    ], "mock"


def combined_source(*sources):
    """If any underlying fetch fell back to mock data, the combined result is "mock" —
    a response is only "live" when every source behind it was real Meraki data."""
    return "mock" if "mock" in sources else "live"


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
    networks, source = fetch_networks()
    return {"networks": networks, "source": source}


@app.route('/devices')
def get_devices():
    devices, source = fetch_devices()
    return {"devices": devices, "source": source}


@app.route('/networks/<network_id>/health')
def get_network_health(network_id):
    networks, networks_source = fetch_networks()
    network = next((n for n in networks if n["id"] == network_id), None)

    if network is None:
        return {"error": f"Network '{network_id}' not found"}, 404

    device_statuses, statuses_source = fetch_device_statuses()
    result = check_network_health(network, device_statuses)
    source = combined_source(networks_source, statuses_source)
    return {"network_id": network_id, "name": network["name"], **result, "source": source}

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
    devices, devices_source = fetch_devices()
    device = next((d for d in devices if d ["serial"] == serial), None)

    if device is None:
        return {"error": f"Device '{serial}' not found"}, 404

    device_statuses, statuses_source = fetch_device_statuses()
    result = check_device_compliance(device, device_statuses)
    source = combined_source(devices_source, statuses_source)
    return {"serial": serial, "name": device["name"], **result, "source": source}
# should print it out the ohome address weblink but adjust it with the compliance and devices url added

@app.route('/alerts/scan', methods = ['POST'])
def scan_alerts():
    networks, networks_source = fetch_networks()
    device_statuses, statuses_source = fetch_device_statuses()
    alerts = []
    source = combined_source(networks_source, statuses_source)

    for network in networks:
        result = check_network_health(network, device_statuses)
        if result["healthy"] == False:
            alerts.append(result["issue"])
        db.session.add(HealthCheck(
            network_id=network["id"],
            network_name=network["name"],
            healthy=result["healthy"],
            issue=result["issue"],
            source=source,
        ))
    db.session.commit()

    return{"alerts_found": len(alerts), "alerts": alerts, "source": source}


@app.route('/alerts/history')
def alert_history():
    """Most recent stored health checks, newest first. Optional ?network_id= and ?limit= (max 200)."""
    limit = min(request.args.get("limit", default=50, type=int), 200)
    query = HealthCheck.query.order_by(HealthCheck.checked_at.desc(), HealthCheck.id.desc())
    network_id = request.args.get("network_id")
    if network_id:
        query = query.filter_by(network_id=network_id)
    return {"history": [row.to_dict() for row in query.limit(limit).all()]}


if __name__ == '__main__':
    app.run(debug=True)