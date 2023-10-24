## pubsub with grpc

### Description:
pubsub is a publish subsribe model with a registry server and multiple servers and clients. Each server represents a different community that a client can join and publish articles to. Client can also subscribe to a subset of the articles from the server. Each communication happens using google protos, that makes the communication machine and language independent.

### Features:
Registry server:
- Registry server maintains a list of registered servers, which it send to the client wheneven it joins.

Server:
- Each server register to the registry server and then listens to incoming client request.
- Before processing any request from the client, server first check whether the client is joined or not.
- Each server can join multiple other servers also. If server A joins server B, then all articles of server B would be available on server A.

Client:
- Each client requests a list of the registered servers from the registry server when it joins.
- A client would have the following features: join server, leave server, publish articles, get articles.
- Each client can join multiple servers.
- Client can request a subset of articles from any server. When client requests for articles, the server uses DFS to fetch the articles from all the servers that it is connected to. This ensures that the server does not get stuck in cycles while fetching articles from other servers.

Connector:
- A connector is a service used to connect two servers together.

### Pre-requisite:
- proto (if you want to make changes to underlying message structures).
- grpc
- python (prefarably latest version)

### Usage:
- Run the registry server using `python registry_server.py`. It will run the registry server on `port 50051`.
- Run the server using `python server.py <port number>`, where port number is a valid available port number.
- Run the client using `python client.py`. The client interface will have a menu that you can use to interact with the server.
- Run the connector using `python connector.py`. This interface can be used to connect two servers.

### Contributing:
If you would like to contribute to the PubSub System, please create a pull request with your changes. I welcome all contributions and appreciate your help in improving the system.

### License:
This project is licensed under the MIT License. See the LICENSE file for more details.