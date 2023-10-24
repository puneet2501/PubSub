from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
FAIL: StatusType
FASHION: ArticleType
NOTYPE: ArticleType
PASS: StatusType
POLITICS: ArticleType
SPORTS: ArticleType

class Article(_message.Message):
    __slots__ = ["author", "content", "timestamp", "type"]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    author: str
    content: str
    timestamp: _timestamp_pb2.Timestamp
    type: ArticleType
    def __init__(self, type: _Optional[_Union[ArticleType, str]] = ..., author: _Optional[str] = ..., content: _Optional[str] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ArticleList(_message.Message):
    __slots__ = ["articles"]
    ARTICLES_FIELD_NUMBER: _ClassVar[int]
    articles: _containers.RepeatedCompositeFieldContainer[Article]
    def __init__(self, articles: _Optional[_Iterable[_Union[Article, _Mapping]]] = ...) -> None: ...

class ArticleRequest(_message.Message):
    __slots__ = ["author", "date", "type", "uid"]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    author: str
    date: _timestamp_pb2.Timestamp
    type: ArticleType
    uid: str
    def __init__(self, author: _Optional[str] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., type: _Optional[_Union[ArticleType, str]] = ..., uid: _Optional[str] = ...) -> None: ...

class ArticlesResponse(_message.Message):
    __slots__ = ["articles", "status"]
    ARTICLES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    articles: _containers.RepeatedCompositeFieldContainer[Article]
    status: StatusType
    def __init__(self, status: _Optional[_Union[StatusType, str]] = ..., articles: _Optional[_Iterable[_Union[Article, _Mapping]]] = ...) -> None: ...

class Client(_message.Message):
    __slots__ = ["name", "uid"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    name: str
    uid: str
    def __init__(self, name: _Optional[str] = ..., uid: _Optional[str] = ...) -> None: ...

class ConnectedGetArticleRequest(_message.Message):
    __slots__ = ["articleRequest", "currentServer", "isClientCheck", "visitedServers"]
    ARTICLEREQUEST_FIELD_NUMBER: _ClassVar[int]
    CURRENTSERVER_FIELD_NUMBER: _ClassVar[int]
    ISCLIENTCHECK_FIELD_NUMBER: _ClassVar[int]
    VISITEDSERVERS_FIELD_NUMBER: _ClassVar[int]
    articleRequest: ArticleRequest
    currentServer: Server
    isClientCheck: bool
    visitedServers: _containers.RepeatedCompositeFieldContainer[Server]
    def __init__(self, articleRequest: _Optional[_Union[ArticleRequest, _Mapping]] = ..., visitedServers: _Optional[_Iterable[_Union[Server, _Mapping]]] = ..., currentServer: _Optional[_Union[Server, _Mapping]] = ..., isClientCheck: bool = ...) -> None: ...

class PublishArticleRequest(_message.Message):
    __slots__ = ["author", "content", "type", "uid"]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    author: str
    content: str
    type: ArticleType
    uid: str
    def __init__(self, type: _Optional[_Union[ArticleType, str]] = ..., author: _Optional[str] = ..., content: _Optional[str] = ..., uid: _Optional[str] = ...) -> None: ...

class Server(_message.Message):
    __slots__ = ["ip", "name", "port"]
    IP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ip: str
    name: str
    port: int
    def __init__(self, name: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class ServerList(_message.Message):
    __slots__ = ["servers"]
    SERVERS_FIELD_NUMBER: _ClassVar[int]
    servers: _containers.RepeatedCompositeFieldContainer[Server]
    def __init__(self, servers: _Optional[_Iterable[_Union[Server, _Mapping]]] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: StatusType
    def __init__(self, status: _Optional[_Union[StatusType, str]] = ...) -> None: ...

class StatusType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ArticleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
