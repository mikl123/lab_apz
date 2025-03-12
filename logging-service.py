from flask import Flask, request, jsonify
import time
import hazelcast
import argparse

app = Flask(__name__)
local_db = {}
delay_time = 3
add_delay = False # needed for retry system check.

hz_client = None
distr_map = None

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

if __name__ == '__main__':
    hz_client = hazelcast.HazelcastClient()
    distr_map = hz_client.get_map("map1").blocking()
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001, help='Port to run the app on')
    args = parser.parse_args()

    app.run(debug=True, port=args.port)