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
from datetime import datetime

REGISTRY_SERVER_IP = "localhost"
REGISTRY_SERVER_PORT = 50051

SERVERS = []
uid = str(uuid.uuid4())
NAME = 'Client' + uid

def printServers():
    print("\nServers: ")
    for i in range(len(SERVERS)):
        print("Server"+str(i+1)+" -", SERVERS[i].ip + ":" + str(SERVERS[i].port))

def getDate(timestamp):
    return datetime.fromtimestamp(timestamp.seconds + timestamp.nanos/1e9)

def getTypeName(type):
    if(type == pubsub_pb2.ArticleType.SPORTS):
        return "SPORTS"
    if(type == pubsub_pb2.ArticleType.FASHION):
        return "FASHION"
    return "POLITICS"

def printArticle(id, article):
    print(str(id+1) + ")" + getTypeName(article.type))
    print(article.author)
    print(getDate(article.timestamp))
    print(article.content)

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(REGISTRY_SERVER_IP + ":" + str(REGISTRY_SERVER_PORT)) as channel:
        stub = pubsub_pb2_grpc.RegisteryServerAndClientServiceStub(channel)
        servers = stub.GetListOfServers(pubsub_pb2.Client(name=NAME, uid=uid))
        
        for server in servers:
            SERVERS.append(server)
        printServers()

    getProtoType = {"": pubsub_pb2.ArticleType.NOTYPE, "1": pubsub_pb2.ArticleType.SPORTS, "2": pubsub_pb2.ArticleType.FASHION, "3": pubsub_pb2.ArticleType.POLITICS}
    while True:
        print("Menu:")
        print("1. Join Server \n2. Leave Server \n3. Get Articles \n4. Publish Article")
        choice = int(input("Enter your choice: "))
        
        if(choice == 1):
            # JoinServer
            printServers()
            id = int(input("Input the server to which you want to connect: "))
            print("Joining server", id)

            with grpc.insecure_channel(SERVERS[id-1].ip + ":" + str(SERVERS[id-1].port)) as channel:
                stub = pubsub_pb2_grpc.ServerAndClientServiceStub(channel)
                response = stub.JoinServer(pubsub_pb2.Client(uid=uid, name=NAME))
                print(response)
            pass
        elif (choice == 2):
            # LeaveServer
            printServers()
            id = int(input("Input the server which you want to leave: "))

            with grpc.insecure_channel(SERVERS[id-1].ip + ":" + str(SERVERS[id-1].port)) as channel:
                stub = pubsub_pb2_grpc.ServerAndClientServiceStub(channel)
                response = stub.LeaveServer(pubsub_pb2.Client(uid=uid, name=NAME))
                print(response)
            pass
        elif(choice == 3):
            # GetAllArticles
            print("\n1. SPORTS \n2. FASHION \n3. POLITICS")
            type = input("Enter article type: ")
            author = input("Enter Author: ")
            date = input("Enter date in the format dd/mm/yyyy: ")
            
            # List of servers to get articles on
            printServers()
            id = int(input("Enter the server from which you want to get articles: "))

            with grpc.insecure_channel(SERVERS[id-1].ip + ":" + str(SERVERS[id-1].port)) as channel:
                stub = pubsub_pb2_grpc.ServerAndClientServiceStub(channel)

                timestamp = Timestamp()
                try:
                    # print("date = ", date)
                    dtobj = datetime.strptime(date, "%d/%m/%Y")
                    # print("Went into try")
                    timestamp = Timestamp()
                    timestamp.FromDatetime(dtobj)
                except:
                    # print("went into except")
                    timestamp = Timestamp()
                
                # print("timestamp = ", timestamp)
                # print("timestamp in nano = ", timestamp.ToNanoseconds())
                
                articleRequest = pubsub_pb2.ArticleRequest(author=author, date=timestamp, type=getProtoType[type], uid=uid)
                response = stub.getConnectedArticles(pubsub_pb2.ConnectedGetArticleRequest(articleRequest=articleRequest, visitedServers=[], currentServer=SERVERS[id-1], isClientCheck = False))
                status, articles = response.status, response.articles
                print(("FAIL" if status == 0 else "PASS"))

                for i in range(len(articles)):
                    printArticle(i, articles[i])
                print()
            pass
        
        elif(choice == 4):
            # PublishArticle
            print("\n1. SPORTS \n2. FASHION \n3. POLITICS")
            type = input("Enter article type: ")
            author = input("Enter Author: ")
            content = input("Enter content: ")
            # type = "1"
            # author = "hitesh"
            # content = "Hi there!"
            
            # List of servers to publish on
            printServers()
            id = int(input("Enter the server to which you want to publish articles: "))
            # id = 1

            with grpc.insecure_channel(SERVERS[id-1].ip + ":" + str(SERVERS[id-1].port)) as channel:
                stub = pubsub_pb2_grpc.ServerAndClientServiceStub(channel)
                response = stub.publishArticle(pubsub_pb2.PublishArticleRequest(type=getProtoType[type], author=author, content=content, uid=uid))
                print(response)
            pass
        else:
            print("Invalid Choice!")


if __name__ == '__main__':
    logging.basicConfig()
    run()
