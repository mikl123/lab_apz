import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc

class LoggingService(service_pb2_grpc.LoggingServiceServicer):
    def __init__(self):
        self.database = {}

    def Send(self, request, context):
        print("----Recieved post request from facade----")
        self.database[request.uuid] = request.msg
        return service_pb2.Status(msg="Message received successfully")

    def getData(self, request, context):
        print("----Recieved get request from facade----")
        data = [service_pb2.MessageData(msg=self.database[msg]) for msg in self.database]
        return service_pb2.Database(data=data)

def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_LoggingServiceServicer_to_server(LoggingService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    start_grpc_server()
