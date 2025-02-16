from flask import Flask, request, jsonify
import time

app = Flask(__name__)
local_db = {}
delay_time = 3
add_delay = True # needed for retry system check.

@app.route('/send', methods=['POST'])
def receive_data():
    """Recieves data from post request and saves in database"""
    global delay_time
    if add_delay:
        time.sleep(delay_time)
    delay_time = delay_time - 1

    data = request.json
    local_db[data['uuid']] = data["msg"]

    print(f"Received msg: {data['msg']}")
    return jsonify({"message": "Data received successfully!"}), 200

@app.route('/get', methods=['GET'])
def get_data():
    """Returns all saved data"""
    print("-------logging-service recieved get request--------")
    return jsonify({"all_messages":list(local_db.values())}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)