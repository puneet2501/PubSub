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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
from google.protobuf.timestamp_pb2 import Timestamp

import logging
import grpc
import pubsub_pb2
import pubsub_pb2_grpc
import uuid

REGISTRY_SERVER_IP = "localhost"
REGISTRY_SERVER_PORT = 50051

SERVERS = []
uid = 'connector client'
name = 'connector client'

def printServers():
    print("\nServers: ")
    for i in range(len(SERVERS)):
        print("Server"+str(i+1)+" -", SERVERS[i].ip + ":" + str(SERVERS[i].port))
    print()

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(REGISTRY_SERVER_IP + ":" + str(REGISTRY_SERVER_PORT)) as channel:
        stub = pubsub_pb2_grpc.RegisteryServerAndClientServiceStub(channel)
        servers = stub.GetListOfServers(pubsub_pb2.Client(uid=uid))
        
        for server in servers:
            SERVERS.append(server)

    while True:
        printServers()
        
        print("Format: Server A join Server B.")
        ids = input("Enter the ids of servers you want to connect: ")
        id1, id2 = [int(id) for id in ids.split()]
        
        print("\nJoining server", id1, "with server", id2, "...")
        with grpc.insecure_channel(SERVERS[id1-1].ip + ":" + str(SERVERS[id1-1].port)) as channel:
            stub = pubsub_pb2_grpc.ServerConnectorServiceStub(channel)
            response = stub.ConnectServer(SERVERS[id2-1])
            print(response)
        pass

if __name__ == '__main__':
    logging.basicConfig()
    run()
