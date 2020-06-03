import socket
from threading import Thread

from zadania13.materials.functions import *


class Server5:
    def __init__(self, ip="0.0.0.0", port=8080):
        self.ip = ip
        self.port = port

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(5)

        print("Server __5__ Start")
        while True:
            try:
                conn, addr = sock.accept()
                conn = ssl.wrap_socket(conn, server_side=True, ca_certs="../certs/client.crt",
                                       certfile="../certs/server.crt",
                                       keyfile="../certs/server.key", ssl_version=ssl.PROTOCOL_TLSv1_2,
                                       cert_reqs=ssl.CERT_REQUIRED)
                cert = conn.getpeercert()
                if not cert or ssl.match_hostname(cert, "client.com"):
                    print("Not correct certificates for: {}".format(addr[0] + ":" + str(addr[1])))
                    print(cert)
                    continue
                thread = Thread(target=rec_messages, args=[conn], daemon=False)
                thread.start()
                print("Connected: {}".format(addr[0] + ":" + str(addr[1])))
                print(cert)
            except ssl.SSLError as e:
                print(e)
                print("Nie udało połączyć się")


s = Server5()
s.start()
