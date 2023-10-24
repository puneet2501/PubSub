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
from google.protobuf.timestamp_pb2 import Timestamp
# from datetime import datetime
import datetime

import logging
import grpc
import sys
import time
import pubsub_pb2
import pubsub_pb2_grpc

MAX_CLIENTS = 10
REGISTRY_SERVER_IP = "localhost"
REGISTRY_SERVER_PORT = 50051
CLIENTS = []
ARTICLES = []
CONNECTED_SERVER = []

class ServerAndClientService(pubsub_pb2_grpc.ServerAndClientServiceServicer):
    def JoinServer(self, request, context):
        print("JOIN REQUEST FROM", request.uid)
        # print("request: %s" % request)

        if(len(CLIENTS) == MAX_CLIENTS):
            print("MAXIMUM LIMIT REACHED")
            return pubsub_pb2.Status(status = pubsub_pb2.StatusType.FAIL)
        
        for client in CLIENTS:
            if(client.uid == request.uid):
                print("CLIENT IS ALREADY CONNECTED. CANT CONNECT AGAIN")
                return pubsub_pb2.Status(status = pubsub_pb2.StatusType.FAIL)

        CLIENTS.append(request)
        print("CLIENT IS CONNECTED TO SERVER")
        return pubsub_pb2.Status(status = pubsub_pb2.StatusType.PASS)

    def LeaveServer(self, request, context):
        print("LEAVE REQUEST FROM", request.uid)
        # print("request = %s" % request)

        ClientInd = -1
        for ind in range(len(CLIENTS)):
            if(CLIENTS[ind].uid == request.uid):
                ClientInd = ind
                break
            
        if(ClientInd ==  -1):
            print("CLIENT IS NOT CONNECTED TO SERVER. ERROR")
            return pubsub_pb2.Status(status = pubsub_pb2.StatusType.FAIL)

        CLIENTS.pop(ClientInd)
        print("REMOVED CLIENT FROM SERVER")
        return pubsub_pb2.Status(status = pubsub_pb2.StatusType.PASS)

    def checkCreteria(self, article, request):
        # print("checking creteria for article and request:")
        # print("Article %s" % article)
        # print("Request %s" % request)
        authorCheckResult = (not request.HasField("author") or request.author == "" or (request.author == article.author))
        typeCheckResult = (not request.HasField("type") or request.type == pubsub_pb2.ArticleType.NOTYPE or (request.type == article.type))
        dateCheckResult = (not request.HasField("date") or (request.date.ToNanoseconds() == 0) or (article.timestamp.ToNanoseconds() >= request.date.ToNanoseconds()))
        # print("request time = ", request.date.ToNanoseconds())
        # print("article time = ", article.timestamp.ToNanoseconds())
        return authorCheckResult and typeCheckResult and dateCheckResult

    def getTypeName(self, type):
        if(type == pubsub_pb2.ArticleType.NOTYPE):
            return "<BLANK>"
        if(type == pubsub_pb2.ArticleType.SPORTS):
            return "SPORTS"
        if(type == pubsub_pb2.ArticleType.FASHION):
            return "FASHION"
        return "POLITICS"

    def getAuthor(self, author):
        if(author == ""):
            return "<BLANK>"
        return author

    def getDate(self, date):
        if(date.ToNanoseconds() == 0):
            return "<BLANK>"
        return datetime.datetime.fromtimestamp(date.seconds + date.nanos/1e9)

    def checkVisited(self, servers, currentServer):
        for server in servers:
            if(server.ip == currentServer.ip and server.port == currentServer.port):
                return True
        return False

    def getConnectedArticles(self, request, context):
        articleRequest, visitedServers, currentServer, isClientCheck = request.articleRequest, request.visitedServers, request.currentServer, request.isClientCheck
        
        if not isClientCheck:
            print("ARTICLES REQUEST FROM", articleRequest.uid)
            print("FOR", self.getTypeName(articleRequest.type) + ", " + self.getAuthor(articleRequest.author) + ",", self.getDate(articleRequest.date))
            
            ClientInd = -1
            for ind in range(len(CLIENTS)):
                if(CLIENTS[ind].uid == articleRequest.uid):
                    ClientInd = ind
                    break
            
            if(ClientInd ==  -1):
                print("CLIENT IS NOT CONNECTED TO SERVER. ERROR")
                return pubsub_pb2.ArticlesResponse(status = pubsub_pb2.StatusType.FAIL, articles = [])

            isClientCheck = True
            pass
        
        if(self.checkVisited(visitedServers, currentServer)):
            return pubsub_pb2.ArticlesResponse(status = pubsub_pb2.StatusType.PASS, articles = [])
        
        visitedServers.append(currentServer)
        
        articles = []
        for article in ARTICLES:
            if(self.checkCreteria(article, articleRequest)):
                articles.append(article)
        
        
        # print("article = ", articles)
        for server in CONNECTED_SERVER:
            with grpc.insecure_channel(server.ip + ":" + str(server.port)) as channel:
                stub = pubsub_pb2_grpc.ServerAndClientServiceStub(channel)
                connectedRequest = pubsub_pb2.ConnectedGetArticleRequest(articleRequest=articleRequest, visitedServers=visitedServers, currentServer=server, isClientCheck = isClientCheck)
                response = stub.getConnectedArticles(connectedRequest)
                # print("response = ", response)
                
                for article in response.articles:
                    articles.append(article)
        
        return pubsub_pb2.ArticlesResponse(status = pubsub_pb2.StatusType.PASS, articles = articles)

    def getArticles(self, request, context):
        print("ARTICLES REQUEST FROM", request.uid)
        print("FOR", self.getTypeName(request.type) + ", " + self.getAuthor(request.author) + ", " + self.getDate(request.date))

        ClientInd = -1
        for ind in range(len(CLIENTS)):
            if(CLIENTS[ind].uid == request.uid):
                ClientInd = ind
                break
        
        if(ClientInd ==  -1):
            print("CLIENT IS NOT CONNECTED TO SERVER. ERROR")
            return pubsub_pb2.ArticlesResponse(status = pubsub_pb2.StatusType.FAIL, articles = [])

        articles = []
        for article in ARTICLES:
            if(self.checkCreteria(article, request)):
                # print(article)
                articles.append(article)
        
        time.sleep(20)
        return pubsub_pb2.ArticlesResponse(status = pubsub_pb2.StatusType.PASS, articles = articles)

    def publishArticle(self, request, context):
        print("ARTICLES PUBLISH FROM", request.uid)

        clientInd = -1
        for ind in range(len(CLIENTS)):
            if(CLIENTS[ind].uid == request.uid):
                clientInd = ind
                break
        
        if(clientInd == -1):
            return pubsub_pb2.Status(status = pubsub_pb2.StatusType.FAIL)
        
        now = time.time()
        seconds = int(now)
        nanos = int((now-seconds)* 10**9)
        timestamp = Timestamp(seconds = seconds, nanos = nanos)
        ARTICLES.append(pubsub_pb2.Article(type=request.type, author=request.author, content=request.content, timestamp=timestamp))
        return pubsub_pb2.Status(status = pubsub_pb2.StatusType.PASS)

class ServerConnectorService(pubsub_pb2_grpc.ServerConnectorServiceServicer):
    def ConnectServer(self, request, context):
        print("CONNECTING SERVER REQUEST FOR SERVER", request.ip, request.port)
        
        for server in CONNECTED_SERVER:
            if(server.ip == request.ip and server.port == request.port):
                print("CONNECTION FAIL")
                return pubsub_pb2.Status(status=pubsub_pb2.StatusType.FAIL)
            
        CONNECTED_SERVER.append(request)
        print("CONNECTION SUCCESS")
        return pubsub_pb2.Status(status=pubsub_pb2.StatusType.PASS)

def serve():
    port = sys.argv[1]          # 0th argument is file name (file.py)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_CLIENTS))
    pubsub_pb2_grpc.add_ServerAndClientServiceServicer_to_server(ServerAndClientService(), server)
    pubsub_pb2_grpc.add_ServerConnectorServiceServicer_to_server(ServerConnectorService(), server)

    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)

    with grpc.insecure_channel(REGISTRY_SERVER_IP + ":" + str(REGISTRY_SERVER_PORT)) as channel:
        stub = pubsub_pb2_grpc.RegisteryServerAndServerServiceStub(channel)
        response = stub.RegisterServer(pubsub_pb2.Server(name="Server"+port, ip="localhost", port=int(port) ))
        print(response)

    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
