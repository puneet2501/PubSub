# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import pubsub_pb2
import pubsub_pb2_grpc

MAX_SERVERS = 10
SERVERS = []

class RegisteryServerAndServerService(pubsub_pb2_grpc.RegisteryServerAndServerServiceServicer):
    def RegisterServer(self, request, context):
        # print("trying to register server")
        # print("request = ", request)
        print("JOIN REQUEST FROM SEREVR", request.ip, request.port)

        # checking if number of servers has reached limit
        if(len(SERVERS) == MAX_SERVERS):
            print("MAXIMUM LIMIT REACHED")
            return pubsub_pb2.Status(status = pubsub_pb2.StatusType.FAIL)

        # check if the server is already there
        for server in SERVERS:
            if(server.ip == request.ip and server.port == request.port):
                return pubsub_pb2.Status(status = pubsub_pb2.StatusType.PASS)

        # adding server to list
        SERVERS.append(pubsub_pb2.Server(name= request.name, ip= request.ip, port=request.port))
        print("SERVER ADDED TO LIST SUCCESSFULLY")

        return pubsub_pb2.Status(status = pubsub_pb2.StatusType.PASS)

class RegisteryServerAndClientService(pubsub_pb2_grpc.RegisteryServerAndClientServiceServicer):
    # TODO: How to handle the case of where a server terminate unexpectedly
    def GetListOfServers(self, request, context):
        print("SERVER LIST REQUEST FROM", request.uid)
        for server in SERVERS:
            yield server

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_SERVERS))
    pubsub_pb2_grpc.add_RegisteryServerAndServerServiceServicer_to_server(RegisteryServerAndServerService(), server)
    pubsub_pb2_grpc.add_RegisteryServerAndClientServiceServicer_to_server(RegisteryServerAndClientService(), server)

    # helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
