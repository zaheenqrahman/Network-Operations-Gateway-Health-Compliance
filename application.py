from flask import Flask
import requests

app = Flask(__name__)

MERAKI_API_KEY = "YOUR_MERAKI_KEY"
MERAKI_BASE = "https://api.meraki.com/api/v1"


def fetch_networks():
    # MOCK — shaped like a real Meraki /organizations/{id}/networks response.
    # Swap the body of this function for the real Meraki call when the key works.
    return [
        {"id": "N_1001", "name": "Main Office", "status": "online", "type": "wireless"},
        {"id": "N_1002", "name": "Branch Office - East", "status": "offline", "type": "wired"},
        {"id": "N_1003", "name": "Data Center VLAN", "status": "online", "type": "vlan"},
    ]

import requests

API_KEY = "fbbfe24120a81a575e4a952714d7ad36f895add8"
print(repr(API_KEY))
print("length:", len(API_KEY))

headers = {"fbbfe24120a81a575e4a952714d7ad36f895add8": API_KEY}
r = requests.get("https://api.meraki.com/api/v1/organizations", headers=headers)
print(r.status_code)
print(r.text)

import os
API_KEY = os.environ.get("fbbfe24120a81a575e4a952714d7ad36f895add8", "your-dev-key-here")




@app.route('/')
def index():
    return 'Hello!'


@app.route('/networks')
def get_networks():
    return {"networks": fetch_networks()}


if __name__ == '__main__':
    app.run(debug=True)