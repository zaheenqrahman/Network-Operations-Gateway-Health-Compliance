import requests
import json
import os

# creates base url variable for use
BASE_URL = os.environ.get("NETOPS_URL", "http://127.0.0.1:5000").rstrip("/")
# the API requires an X-API-Token header, read from the environment so it never lives in the repo
HEADERS = {"X-API-Token": os.environ.get("GATEWAY_TOKEN", "")}
report = []

response = requests.get(f"{BASE_URL}/networks", headers=HEADERS, timeout=30)
response.raise_for_status()  # 401 here means GATEWAY_TOKEN is missing or wrong
networks = response.json()

for network in networks["networks"]:
    # gets this network id
    network_id = network["id"]
    # builds the health check url with f string
    health_url = f"{BASE_URL}/networks/{network_id}/health"
    # calls the health endpoint check, this is to make sure the data from the API is healthy and cleaned out
    health_response = requests.get(health_url, headers=HEADERS, timeout=30)
    health_response.raise_for_status()
    health_data = health_response.json()

    if health_data["healthy"] == False:
        print (f"⚠️  ALERT: {health_data['issue']}") # alert if the server or network branch is down
        report.append(health_data["issue"])
    else:
        print(f"✅ {network['name']} is healthy")

with open("report.json", "w") as f:
    json.dump(report, f, indent = 2)

# report saves itself and creation of report in json file
print(f"\nReport saved with {len(report)} issue(s).")