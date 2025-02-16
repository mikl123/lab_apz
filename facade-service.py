from flask import Flask, request, jsonify, make_response
import requests
import uuid
import time

app = Flask(__name__)

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
    data = request.json
    random_uuid = uuid.uuid4()

    print(f"-------Facade-service recieved message {data['msg']}--------")
    
    data["uuid"] = str(random_uuid)

    print(f"-------Facade-service generated uuid and sends {data} to logging-service---------")

    response = make_request_with_retry("http://localhost:5001/send", data = data, request_type = "post")

    if response.status_code == 200:
        return jsonify({"message": "Data sent successfully!"}), 200
    else:
        return jsonify({"message": "Failed to send data"}), 500

@app.route('/get', methods=['GET'])
def get_data():
    print("-------Facade-service recived Get request--------")
    response1 = make_request_with_retry("http://localhost:5001/get", request_type = "get")
    response2 = make_request_with_retry("http://localhost:5002/get", request_type = "get")

    print("-------Facade-service returning data from message-service and logging-service.----------")

    if response1.status_code == 200 and response2.status_code == 200:
        return jsonify({"massage-service": response2.json(),
                        "logging-service": response1.json()}), 200
    else:
        return jsonify({"message": "Failed to recieve data"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
