from flask import Flask, jsonify, request
import json

app = Flask(__name__)
local_db = {}

@app.route('/get_ip', methods=['GET'])
def receive_ip():
    service_name = request.args.get('service_name')
    try:
        with open('ip-config.json', 'r') as file:
            data = json.load(file)
    except Exception:
        print('error oppening file with ip config')
        return

    return jsonify({"ips": data[service_name]}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5005)