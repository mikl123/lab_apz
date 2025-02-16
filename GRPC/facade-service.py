from flask import Flask, request, jsonify, make_response
import uuid
from google.protobuf.empty_pb2 import Empty
import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc


app = Flask(__name__)
@app.route('/send', methods=['POST'])
def send_data():
    data = request.json
    random_uuid = uuid.uuid4()

    print(f"----Facade-service recieved message {data['msg']}----")
    
    data["uuid"] = str(random_uuid)

    print(f"----Facade-service generated uuid and sends {data} to logging-service----")

    response = stub.Send(service_pb2.MessageData(msg = data["msg"], uuid = data["uuid"]))

    return jsonify({"message": response.msg})


@app.route('/get', methods=['GET'])
def get_data():
    print("----Facade-service recived Get request----")

    response1 = stub.getData(service_pb2.Empty())
    response2 = stub1.getData(service_pb2.Empty())

    print("----Facade-service returning data from message-service and logging-service.----")
    messages = [message.msg for message in response1.data]
    return jsonify({"messages_logging_service": messages, "messages_message_service":response2.msg})


if __name__ == '__main__':
    channel = grpc.insecure_channel('localhost:50051')
    stub = service_pb2_grpc.LoggingServiceStub(channel)

    channel1 = grpc.insecure_channel('localhost:50052')
    stub1 = service_pb2_grpc.MessageServiceStub(channel1)

    app.run(debug=True, port=5000)

