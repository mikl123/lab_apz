from flask import Flask, request, jsonify
import time
import hazelcast
import argparse
from consul import Consul
import json
app = Flask(__name__)
local_db = {}
delay_time = 3
add_delay = False

hz_client = None
distr_map = None

consul = Consul(host='localhost', port=8500)

def get_map_name():
    _, data = consul.kv.get('config/hazelcast')
    config = None
    if data:
        json_data = data['Value'].decode('utf-8')
        config = json.loads(json_data)
        print("Reading kafka setup:", config)
    else:
        print("Cannot read kafka setup from consul.")
    return config["service"]["map"]

@app.route('/send', methods=['POST'])
def receive_data():
    """Recieves data from post request and saves in database"""
    global delay_time
    if add_delay:
        time.sleep(delay_time)
    delay_time = delay_time - 1

    data = request.json
    distr_map.put(data['uuid'], data["msg"])

    print(f"Received msg: {data['msg']}")
    return jsonify({"message": "Data received successfully!"}), 200

@app.route('/get', methods=['GET'])
def get_data():
    """Returns all saved data"""
    print("-------logging-service recieved get request--------")
    return jsonify({"all_messages":list(distr_map.values())}), 200

@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    hz_client = hazelcast.HazelcastClient()
    distr_map = hz_client.get_map(get_map_name()).blocking()
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001, help='Port to run the app on')
    args = parser.parse_args()
    consul.agent.service.register(
        'logging-service',
        service_id=f'logging-service-id-{args.port}',
        port=args.port,
        tags=['go'],                 
        check={
            'http': f'http://{YOUR_IP}:{args.port}/health',
            'interval': '10s'
        }
    )
    print("Added to consule")
    app.run(debug=True,host="0.0.0.0", port=args.port)