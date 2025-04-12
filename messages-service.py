from flask import Flask, jsonify
from confluent_kafka import Consumer, TopicPartition
import argparse
import threading
part = 0
messages = []

seen_offsets = set()
messages_lock = threading.Lock()

def run_consumer():
    conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'group.id': f'group_message_service_{part}',
    'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    print("Kafka consumer started")
    topic_partition = TopicPartition('messages', part)
    consumer.assign([topic_partition])

    while True:
        msg = consumer.poll(1)
        if msg is None:
            continue
        if msg.error():
            print('Error:', msg.error())
        else:
            with messages_lock:
                messages.append(msg.value().decode('utf-8'))

app = Flask(__name__)
local_db = {}

messages = []
@app.route('/get', methods=['GET'])
def receive_data():
    """Recieves data from post request"""
    print("--------message-service recieved get request--------")
    print("Recieved messages", messages)
    return jsonify({"message": messages}), 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001, help='Port to run the app on')
    parser.add_argument('--partition', type=int, default=0, help='Partition to use')
    args = parser.parse_args()
    part = args.partition
    threading.Thread(target=run_consumer, daemon=True).start()
    app.run(debug=True, port=args.port)

    # consumer.close()
