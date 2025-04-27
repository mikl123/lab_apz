from flask import Flask, request, jsonify, make_response
import requests
import uuid
import time
import random
from confluent_kafka import Producer
from consul import Consul
import json

app = Flask(__name__)

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
    print(config)
    return ",".join([f"localhost:{port}" for port in config["service"]["ports"]])
    
conf = {
    'bootstrap.servers': get_kafka_adresses(),
}

def delivery_report(err, msg):
    if err is not None:
        print('Delivery failed:', err)
    else:
        print('Message delivered to', msg.topic(), msg.partition())

producer = Producer(conf)


def get_ip_address(service_name):
    """This functions seeks int consule available adresses for give service_name"""
    try:
        services = consul.health.service(service_name)
        if not services:
            print(f"No services found for '{service_name}'")
            return None
        ip_port_pairs = []
        for service in services[1]:
            port = service["Service"]["Port"]
            if service['Checks'][-1]['Status'] == 'passing':
                ip_port_pairs.append(port)
        if len(ip_port_pairs) >= 1:
            selected_port = random.choice(ip_port_pairs)
        print("All ports available for " ,service_name , " " ,  ip_port_pairs)
        return f"http://localhost:{selected_port}"
    except Exception as e:
        print(f"Error getting IP address for service '{service_name}': {str(e)}")
        return None

def make_request_with_retry(request, data = None, request_type = "post", n_retries = 3, delay_between_retry = 1, timeout = 2):
    response = 1
    for attempt in range(n_retries):
        print(f"Attempt  {attempt + 1} {request}.")
        try:
            if request_type == "post":
                response = requests.post(request, json=data, timeout = timeout)
            elif request_type == "get":
                response = requests.get(request, json=data, timeout = timeout)
            if response.status_code == 200:
                print(f"Response recieved from {request}")
                return response
            else:
                print(f"Error: {response.status_code} - Retrying...")
        except requests.Timeout:
            print(f"Request timed out after {timeout} seconds - Retrying...")
        except requests.RequestException as e:
            print(f"Exception occurred: {e} - Retrying...")
        time.sleep(delay_between_retry)
    print("All attempts failed")
    response = make_response("Internal Server Error", 500)
    return response

@app.route('/send', methods=['POST'])
def send_data():

    random_ip = get_ip_address('logging-service')
    print(random_ip)
    if not random_ip:
        return jsonify({"message": "Failed to get ip adress"}), 500

    data = request.json
    random_uuid = uuid.uuid4()

    print(f"-------Facade-service recieved message {data['msg']}--------")
    
    data["uuid"] = str(random_uuid)

    print(f"-------Facade-service generated uuid and sends {data} to logging-service---------")

    response = make_request_with_retry(f"{random_ip}/send", data = data, request_type = "post")
    partition = random.randint(0,1)
    print(partition)
    producer.produce('messages', partition = partition, value=data['msg'], callback=delivery_report)
    producer.flush()

    if response.status_code == 200:
        return jsonify({"message": "Data sent successfully!"}), 200
    else:
        return jsonify({"message": "Failed to send data"}), 500

@app.route('/get', methods=['GET'])
def get_data():
    print("-------Facade-service recived Get request--------")
    random_ip_logging = get_ip_address('logging-service')
    if not random_ip_logging:
        return jsonify({"message": "Failed to get ip adress"}), 500
    random_ip_message = get_ip_address('message-service')
    if not random_ip_message:
        return jsonify({"message": "Failed to get ip adress"}), 500
    print('Used ',random_ip_logging, ' as logging service')
    response1 = make_request_with_retry(f"{random_ip_logging}/get", request_type = "get")
    response2 = make_request_with_retry(f"{random_ip_message}/get", request_type = "get")

    print("-------Facade-service returning data from message-service and logging-service.----------")

    if response1.status_code == 200 and response2.status_code == 200:
        return jsonify({"massage-service": response2.json(),
                        "logging-service": response1.json()}), 200
    else:
        return jsonify({"message": "Failed to recieve data"}), 500
    
@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    port = 5000
    consul.agent.service.register(
        'facade-service',
        service_id=f'facade-id-{port}',
        port=port,
        tags=['go'],                 
        check={
            'http': f'http://{YOUR_IP}:{port}/health',
            'interval': '10s'
        }
    )
    app.run(debug=True, host="0.0.0.0", port=5000)
