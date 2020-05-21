from zadania10.functions import *
from threading import Thread
from zadania11.server1 import Server
from socket import error
from datetime import datetime


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
        while True:
            try:
                command = get_command(self.conn).replace(b" ", b"").replace(b"\r\n", b"")
                print("Command:", command, "++")
                splt_com = command.split(b":")
                command = splt_com[0].lower()
                run_com[command](self.conn, splt_com[1:])
            except error as e:
                print("Error:", e)
                break
            except KeyError:
                print("Command not found!!!")
                self.conn.sendall(b"ERROR\r\n")


def fun(conn, addr):
    f = open("log.txt", "a")
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
    f.write(dt_string + "  --------  IP: " + str(addr[0]) + "  PORT: " + str(addr[1]) + "\n")
    f.close()


run_com = {b"get_image": get_image, b"list_images": list_images}
s = Server("localhost", 125, ClientThread, fun)
s.run()
