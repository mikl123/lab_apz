from flask import Flask, jsonify
from confluent_kafka import Consumer, TopicPartition
import argparse
import threading
from consul import Consul
import json

part = 0
messages = []

seen_offsets = set()
messages_lock = threading.Lock()
consul = Consul(host='localhost', port=8500)

def get_kafka_adresses():
    _, data = consul.kv.get('config/kafka')
    config = None
    if data:
        json_data = data['Value'].decode('utf-8')
        config = json.loads(json_data)
        print("Reading kafka setup:", config)
    else:
        print("Cannot read kafka setup from consul.")
    return ",".join([f"localhost:{port}" for port in config["service"]["ports"]])

def run_consumer():
    conf = {
    'bootstrap.servers': get_kafka_adresses(),
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

@app.route('/health')
def health_check():
    return 'OK', 200


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

    service_name = "message-service"
    port = args.port

    service_id = f"message-service-id-{port}"

    check = {
        "http": f"http://{YOUR_IP}:{port}/health",
        "interval": "10s",
        "timeout": "5s",
    }

    consul.agent.service.register(
        service_name,
        service_id=service_id,
        port=port,
        tags=["go"],
        check=check
    )


    app.run(debug=True, host='0.0.0.0', port=args.port)

    # consumer.close()
