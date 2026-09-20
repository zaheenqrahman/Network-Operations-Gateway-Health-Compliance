import requests
import json

# creates base url variable for use
BASE_URL = "http://127.0.0.1:5000"
report = [] # establishes report variable calling from API

response = requests.get('http://127.0.0.1:5000/networks')
networks = response.json()

for network in networks["networks"]:
    # gets this network id
    network_id = network["id"]
    # builds the health check url with f string
    health_url = f"{BASE_URL}/networks/{network_id}/health"
    # calls the health endpoint check, this is to make sure the data from the API is healthy and cleaned out
    health_response = requests.get(health_url)
    health_data = health_response.json()

    if health_data["healthy"] == False:
        print (f"⚠️  ALERT: {health_data['issue']}") # alert if the server or network branch is down
        report.append(health_data["issue"])
    else:
        print(f"✅ {network['name']} is healthy") # other server/network branches are up

with open("report.json", "w") as f:
    json.dump(report, f, indent = 2)

# report saves itself and creation of report in json file
print(f"\nReport saved with {len(report)} issue(s).")