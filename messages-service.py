from flask import Flask, jsonify
from confluent_kafka import Consumer
import argparse

app = Flask(__name__)
local_db = {}
conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
}
messages = []
@app.route('/get', methods=['GET'])
def receive_data():
    """Recieves data from post request"""
    print("--------message-service recieved get request--------")

    return jsonify({"message": messages}), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001, help='Port to run the app on')
    args = parser.parse_args()
    app.run(debug=True, port=args.port)
    consumer = Consumer(conf)
    consumer.subscribe(['messages'])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            messages.append(msg)
        if msg.error():
            print('Error:', msg.error())
        else:
            print(f"Received: {msg.value().decode('utf-8')} from partition {msg.partition()}")

    # consumer.close()
