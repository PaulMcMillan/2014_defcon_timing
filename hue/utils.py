
# Monkeypatch requests to use TCP_NODELAY
from requests.packages.urllib3 import connectionpool

_HTTPConnection = connectionpool.HTTPConnection
_HTTPSConnection = connectionpool.HTTPSConnection

class HTTPConnection(_HTTPConnection):
    def connect(self):
        _HTTPConnection.connect(self)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
#        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 0)

class HTTPSConnection(_HTTPSConnection):
    def connect(self):
        _HTTPSConnection.connect(self)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
#        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 0)


connectionpool.HTTPConnection = HTTPConnection
connectionpool.HTTPSConnection = HTTPSConnection
