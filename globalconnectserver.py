import socket, threading, sys

SERVER_TO_CLIENT = "client"
CLIENT_TO_SERVER = "server"

class Connection(object):
    def __init__(self, conn: socket.socket, addr: tuple, redirAddr: tuple, routes: list):
        self.conn = conn
        self.addr = addr
        self.REDIR_TO = redirAddr

        self.routes = routes

        self.client_to_server_inter = None
        self.server_to_client_inter = None

        for route in self.routes:
            if route[0] == "client":
                self.server_to_client_inter = route[1]
            elif route[0] == "server":
                self.client_to_server_inter = route[1]


        self.ServerSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSoc.connect(self.REDIR_TO)
        print(f"Connected to {self.REDIR_TO[0]}:{self.REDIR_TO[1]}")
    
    def _client_to_server(self):
        try:
            while True:
                data = self.conn.recv(8024)
                if self.client_to_server_inter != None:
                    data = self.client_to_server_inter(data)
                if len(data) != 0:
                    self.ServerSoc.send(data)
        except ConnectionAbortedError:
            print(f"Connection aborted {self.addr[0]}:{self.addr[1]} -> {self.REDIR_TO[0]}:{self.REDIR_TO[1]}")
    
    def _server_to_client(self):
        try:
            while True:
                data = self.ServerSoc.recv(8024)
                if self.server_to_client_inter != None:
                    data = self.server_to_client_inter(data)
                if len(data) != 0:
                    self.conn.send(data)
        except ConnectionAbortedError:
            print(f"Connection aborted {self.REDIR_TO[0]}:{self.REDIR_TO[1]} -> {self.addr[0]}:{self.addr[1]}")

    def run(self):
        print(f"Starting forwarder {self.addr[0]}:{self.addr[1]} -> {self.REDIR_TO[0]}:{self.REDIR_TO[1]}")
        threading.Thread(target=self._client_to_server).start()
        threading.Thread(target=self._server_to_client).start()

class Server(object):
    def __init__(self, RECV_ADDR: tuple, REDIR_ADDR: tuple):
        self.RECV_ADDR = RECV_ADDR
        self.REDIR_ADDR = REDIR_ADDR

        self.connections = []
        self.routes      = []
    
    def route(self, name: str):
        def decorator(func):
            self.routes.append((name, func))
            return func
        return decorator

    def start(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(self.RECV_ADDR)
        self.soc.listen(5)
        print(f"Listening on {self.RECV_ADDR[0]}:{self.RECV_ADDR[1]}")
        while True:
            conn, addr = self.soc.accept()
            print(f"Recived connection from {addr[0]}:{addr[1]}")
            conec = Connection(conn, self.RECV_ADDR, self.REDIR_ADDR, self.routes)
            threading.Thread(target=conec.run).start()

recvIp    = sys.argv[1]
recvPort  = int(sys.argv[2])
redirIp   = sys.argv[3]
redirPort = int(sys.argv[4])

print(f"{recvIp}:{recvPort} -> {redirIp}:{redirPort}")
NewServer = Server((recvIp, recvPort), (redirIp, redirPort))
NewServer.start()