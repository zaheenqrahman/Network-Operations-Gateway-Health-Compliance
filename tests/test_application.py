import pytest

from application import app, check_device_compliance, check_network_health


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --- check_network_health ---

def test_network_health_online():
    network = {"id": "N_1001", "name": "Main Office"}
    device_statuses = [{"serial": "Q2XX-XXXX-0001", "networkId": "N_1001", "status": "online"}]
    result = check_network_health(network, device_statuses)
    assert result == {"healthy": True, "issue": None}


def test_network_health_offline():
    network = {"id": "N_1002", "name": "Branch Office - East"}
    device_statuses = [
        {"serial": "Q2XX-XXXX-0003", "name": "Branch-Switch", "networkId": "N_1002", "status": "offline"}
    ]
    result = check_network_health(network, device_statuses)
    assert result["healthy"] is False
    assert result["issue"] == "Network 'Branch Office - East' has device(s) down: Branch-Switch"


# --- check_device_compliance ---

def test_device_compliance_online_approved_model():
    device = {"serial": "Q2XX-XXXX-0001", "model": "MR20"}
    device_statuses = [{"serial": "Q2XX-XXXX-0001", "status": "online"}]
    result = check_device_compliance(device, device_statuses)
    assert result == {"compliant": True, "issues": []}


def test_device_compliance_offline_device():
    device = {"serial": "Q2XX-XXXX-0001", "model": "MR20"}
    device_statuses = [{"serial": "Q2XX-XXXX-0001", "status": "offline"}]
    result = check_device_compliance(device, device_statuses)
    assert result["compliant"] is False
    assert "Device is offline" in result["issues"]


def test_device_compliance_unapproved_model():
    device = {"serial": "Q2XX-XXXX-0001", "model": "UnknownModel"}
    device_statuses = [{"serial": "Q2XX-XXXX-0001", "status": "online"}]
    result = check_device_compliance(device, device_statuses)
    assert result["compliant"] is False
    assert "Model UnknownModel is not on the approved list" in result["issues"]


def test_device_compliance_offline_and_unapproved_model():
    device = {"serial": "Q2XX-XXXX-0001", "model": "UnknownModel"}
    device_statuses = [{"serial": "Q2XX-XXXX-0001", "status": "offline"}]
    result = check_device_compliance(device, device_statuses)
    assert result["compliant"] is False
    assert len(result["issues"]) == 2


# --- routes ---

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Hello!"


def test_get_networks(client):
    response = client.get("/networks")
    assert response.status_code == 200
    data = response.get_json()
    assert "networks" in data
    assert len(data["networks"]) > 0
    assert data["source"] in ("live", "mock")


def test_get_devices(client):
    response = client.get("/devices")
    assert response.status_code == 200
    data = response.get_json()
    assert "devices" in data
    assert len(data["devices"]) > 0
    assert data["source"] in ("live", "mock")


def test_network_health_route_found(client):
    networks = client.get("/networks").get_json()["networks"]
    network_id = networks[0]["id"]

    response = client.get(f"/networks/{network_id}/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["network_id"] == network_id
    assert "healthy" in data
    assert data["source"] in ("live", "mock")


def test_network_health_route_not_found(client):
    response = client.get("/networks/does-not-exist/health")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_device_compliance_route_found(client):
    devices = client.get("/devices").get_json()["devices"]
    serial = devices[0]["serial"]

    response = client.get(f"/devices/{serial}/compliance")
    assert response.status_code == 200
    data = response.get_json()
    assert data["serial"] == serial
    assert "compliant" in data
    assert data["source"] in ("live", "mock")


def test_device_compliance_route_not_found(client):
    response = client.get("/devices/does-not-exist/compliance")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_alerts_scan(client):
    response = client.post("/alerts/scan")
    assert response.status_code == 200
    data = response.get_json()
    assert "alerts_found" in data
    assert data["alerts_found"] == len(data["alerts"])
    assert data["source"] in ("live", "mock")
