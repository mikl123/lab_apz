import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc

local_db = {}

class MessageService(service_pb2_grpc.MessageServiceServicer):
    def getData(self, request, context):
        print("----Recieved request from facade----")
        return service_pb2.Status(msg="For now just hello :)")

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MessageServiceServicer_to_server(MessageService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("gRPC server running on port 50052")
    server.wait_for_termination()