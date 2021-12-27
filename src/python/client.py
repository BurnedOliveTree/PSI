import logging, sys
from lib.SocketInterface import SocketInterface
from lib.TCP.ClientSocketTCP import ClientSocket as SocketTCP
from lib.UDP.SocketUDP import SocketUDP as SocketUDP
from lib.Host import Host, get_project_root

class Client(Host):
    def __init__(self, argv: list):
        super().__init__(argv)
        self.send_type_is_struct = False

    def connect(self) -> None:
        self.__get_input_type()
        socket = self.__get_socket()
        with SocketInterface(socket) as socket:
            if socket is not None:
                print("Will send data to ", self.host, ":", self.port)
                data = self.__get_user_data()
                while data != "QUIT":
                    socket.send(data, is_struct=self.send_type_is_struct)
                    received_data = socket.read()
                    print('Received data: ', repr(received_data))
                    data = self.__get_user_data()
                else:
                    socket.send(data)
            else:
                print('Failed to connect, exiting now...')
        print('Client finished')
    
    def __get_socket(self):
        if self.protocol == 'UDP':
            return SocketUDP(self.host, self.port)
        elif self.protocol == 'TCP':
            return SocketTCP(self.host, self.port)
        else:
            raise ValueError(f'invalid protocol type: {self.protocol} please choose from UDP or TCP')

    def __input(self, msg: str):
        try:
            return input(msg)
        except KeyboardInterrupt:
            return None

    def __get_user_data(self) -> str:
        if self.send_type_is_struct:
            return self.__input("Press Enter to send struct or type 'QUIT': ")
        data = self.__input("Data: ")
        if data == "":
            return self.__get_long_text()
        return data
    
    def __get_long_text(self):
        file = open(get_project_root() + '/src/python/text.txt', mode='r')
        text = file.read()
        file.close()
        return text

    def __get_input_type(self) -> bool:
        input_type = self.__input("Choose type of sending data: \n 1.string\n 2.struct\nYour choice: ")
        try:
            option = int(input_type)
            if option == 2:
                self.send_type_is_struct = True
        except ValueError:
            print("Wrong input! Sending default input type - string")


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=get_project_root()+'/log/client.log',
        level=logging.DEBUG
    )
    Client(sys.argv).connect()
    
