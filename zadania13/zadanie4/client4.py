import socket

from zadania13.materials.functions import input_user, recv_all, connect


class Client:
    def __init__(self, conn, server_host_name, ca_cert="", cert="", key=""):
        self.conn = conn
        self.server_host = server_host_name
        self.key = key
        self.cert = cert
        self.ca_cert = ca_cert

        self.conn = connect(self.conn, server_host_name, ca_cert, cert, key)

    def send_rec_mes(self, max_size=1024):
        while True:
            mes = input_user("Message: ")
            if mes == b"q":
                break
            if len(mes) > max_size:
                continue
            self.conn.sendall(mes + b"\r\n")
            print(recv_all(self.conn, 1024)[:-2].decode("utf-8"))


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect(("127.0.0.1", 8080))
    client = Client(sock, "okotyk.com", ca_cert="../certs/server.crt")
    client.send_rec_mes()
