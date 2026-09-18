from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello!'

@app.route('/networks')
def get_networks():
    # Mock data — shaped like a real Meraki /networks response.
    # Swap this for a real Meraki API call later if time allows.
    return {
        "networks": [
            {"id": "N_1001", "name": "Main Office", "status": "online", "type": "wireless"},
            {"id": "N_1002", "name": "Branch Office - East", "status": "offline", "type": "wired"},
            {"id": "N_1003", "name": "Data Center VLAN", "status": "online", "type": "vlan"}
        ]
    }

if __name__ == '__main__':
    app.run(debug=True)