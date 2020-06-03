import socket
from threading import Thread

from zadania13.materials.functions import *


class Server4:
    def __init__(self, ip="0.0.0.0", port=8080):
        self.ip = ip
        self.port = port

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(5)

        print("Server __4__  Start")
        while True:
            conn, addr = sock.accept()
            conn = ssl.wrap_socket(conn, server_side=True, certfile="../certs/server.crt",
                                   keyfile="../certs/server.key", ssl_version=ssl.PROTOCOL_TLSv1_2)
            thread = Thread(target=rec_messages, args=[conn], daemon=False)
            thread.start()
            print("Connected: {}".format(addr[0] + ":" + str(addr[1])))


s = Server4()
s.start()
