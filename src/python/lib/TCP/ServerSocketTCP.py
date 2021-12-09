from io import BytesIO
import struct
from lib.TCP.SocketTCP import SocketTCP
from lib.RawSocket import RawSocket
from select import poll, POLLIN
import logging

class ServerSocket(SocketTCP):
    def __init__(self, host: str, port: str):
        super().__init__(host, port)
        self.poll = poll()
        self.main_socket: RawSocket = None
        self.sockets: dict[int, RawSocket] = {}

    def read(self):
        sockets_answer = []
        for fd, socket in [(fd, self.sockets[fd]) for fd, _ in self.poll.poll()]:
            sockets_answer.append((fd, super().read(socket=socket)))
        return sockets_answer
    
    def send(self, binary_stream: BytesIO, fd: int):
        super().send(binary_stream, socket = self.sockets[fd])

    def connect(self) -> None or bool:
        if not self.main_socket:
            self.main_socket = RawSocket("ipv6" if ":" in self.host else "ipv4", "TCP")
            if self.main_socket.bind(self.host, self.port) == False:
                return False
            self.main_socket.listen(1)  # TODO change this magic number
        accept_returns = self.main_socket.accept()
        if accept_returns == False:
            return False
        socket, _ = accept_returns
        self.poll.register(socket.fileno(), POLLIN)
        self.sockets[socket.fileno()] = RawSocket(created_socket = socket)
        logging.info('Using TCP socket')

    def disconnect(self, fd: int = None) -> None:
        if fd:
            self.poll.unregister(fd)
            self.sockets[fd].disconnect()
            self.sockets.pop(fd)
        else:
            if self.main_socket:
                self.main_socket.disconnect()
                self.main_socket = None
            if self.sockets:
                for fd, socket in self.sockets.items():
                    self.poll.unregister(fd)
                    socket.disconnect()
                self.sockets = {}