import pytest

from application import app, check_device_compliance, check_network_health


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --- check_network_health ---

def test_network_health_online():
    result = check_network_health({"name": "Main Office", "status": "online"})
    assert result == {"healthy": True, "issue": None}


def test_network_health_offline():
    result = check_network_health({"name": "Branch Office - East", "status": "offline"})
    assert result["healthy"] is False
    assert result["issue"] == "Network 'Branch Office - East' is offline"


# --- check_device_compliance ---

def test_device_compliance_online_approved_model():
    result = check_device_compliance({"status": "online", "model": "MR20"})
    assert result == {"compliant": True, "issues": []}


def test_device_compliance_offline_device():
    result = check_device_compliance({"status": "offline", "model": "MR20"})
    assert result["compliant"] is False
    assert "Device is offline" in result["issues"]


def test_device_compliance_unapproved_model():
    result = check_device_compliance({"status": "online", "model": "UnknownModel"})
    assert result["compliant"] is False
    assert "Model UnknownModel is not on the approved list" in result["issues"]


def test_device_compliance_offline_and_unapproved_model():
    result = check_device_compliance({"status": "offline", "model": "UnknownModel"})
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


def test_get_devices(client):
    response = client.get("/devices")
    assert response.status_code == 200
    data = response.get_json()
    assert "devices" in data
    assert len(data["devices"]) > 0


def test_network_health_route_found(client):
    networks = client.get("/networks").get_json()["networks"]
    network_id = networks[0]["id"]

    response = client.get(f"/networks/{network_id}/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["network_id"] == network_id
    assert "healthy" in data


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
