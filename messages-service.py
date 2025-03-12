from flask import Flask, jsonify

app = Flask(__name__)
local_db = {}

@app.route('/get', methods=['GET'])
def receive_data():
    """Recieves data from post request"""
    print("--------message-service recieved get request--------")

    return jsonify({"message": "Not implemented yet"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5004)