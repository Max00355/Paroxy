import socket
import threading
import re

class Paroxy:

    def __init__(self):
        self.port = 8081
        self.sock = socket.socket()
        self.host = "0.0.0.0"

    def main(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        while True:
            obj, conn = self.sock.accept()
            threading.Thread(target=self.handle, args=(obj,)).start()

    def handle(self, obj):
        data_ = obj.recv(1024)
        if data_:
            data = data_.replace("\r", '')
            host = re.findall("Host: (.*)", data)[0]
            print host
            sock = socket.socket()
            sock.connect((host, 80))
            sock.send(data_)
            data = ""
            while True:
                d = sock.recv(1024)
                if d:
                    data = data+d
                else:
                    sock.close()
                    break
            obj.send(data)
            obj.close()
        else:
            obj.close()

if __name__ == "__main__":
    Paroxy().main()
