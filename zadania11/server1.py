from socket import AF_INET, SOCK_STREAM, socket, error
from threading import Thread


def fun(conn, addr):
    print("Connection:", addr)


class ClientThread(Thread):
    def __init__(self, connection, addr):
        ip = str(s.ip).encode("utf-8")
        port = str(s.port).encode("utf-8")
        connection.sendall(
            b"You are connected to ---  ip:" + ip + b" ---- post: " + port)
        self.conn = connection
        self.addr = addr
        Thread.__init__(self)

    def run(self):
        try:
            while True:
                self.conn.settimeout(30)
                data = self.conn.recv(1024)
                self.conn.sendall(data)
                print(self.addr, "DATA: ", data)
        except error as e:
            print(self.addr, "ERROR:", e)
            print(self.addr, "CLOSED:")
        # obsluga odbierania i wysylania danych


class Server:
    def __init__(self, ip, port, klass, on_connect=fun):
        self.ip = ip
        self.port = port
        self.klass = klass
        self.on_connect = on_connect
        print("Server start!!!")

    def run(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(10)

        try:
            while True:
                conn, addr = sock.accept()
                c = self.klass(conn, addr)
                c.start()
                self.on_connect(conn, addr)
        except error as e:
            print(e)


if __name__ == "__main__":
    s = Server("localhost", 125, ClientThread)
    s.run()
