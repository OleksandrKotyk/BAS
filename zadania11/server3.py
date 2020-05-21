from socket import error
from threading import Thread
from zadania11.server1 import Server, fun
from random import randint


class ClientThread(Thread):
    def __init__(self, connection, addr):
        ip = str(s.ip).encode("utf-8")
        port = str(s.port).encode("utf-8")
        self.max_count = 15
        max_count = self.max_count.__str__().encode("utf-8")
        connection.sendall(
            b"Gra zaczyna sie, liczba od 0 do 100, wpisz -1 zeby odzyskac liczbe, masz " + max_count +
            b" ilosc prob --- ip:" + ip + b" --- post: " + port)
        self.conn = connection
        self.addr = addr
        self.rand_n = randint(1, 100)
        self.counter = 0
        Thread.__init__(self)

    def run(self):
        self.conn.settimeout(30)
        try:
            while True:
                data = self.conn.recv(1024)
                try:
                    num = int(data)
                except ValueError:
                    self.conn.sendall(b"Error!!!")
                    continue

                self.counter += 1
                add = b""
                if self.counter == self.max_count:
                    add = b" Nie masz juz sprob!!!"

                if num == -1:
                    self.conn.sendall(b"Licaba = " + str(self.rand_n).encode("utf-8") + b"\nGoodbye!!!")
                    self.conn.close()
                    raise error("Zakonczony przez klienta, klient przegral")

                if num < self.rand_n:
                    self.conn.sendall(b"Mniejsza od wylosowanej przez serwer!!!" + add)
                elif num > self.rand_n:
                    self.conn.sendall(b"Wieksza od wylosowanej przez serwer!!!" + add)
                else:
                    self.conn.sendall(b"Rowna wylosowanej przez serwer!!!" + add)
                    raise error("Zakonczony przez klienta, klient wygral")

                if add != b"":
                    raise error("Zakonczony przez klienta, klient przegral ilosc raz")

                print(self.addr, "NUMBER: ", num)

        except error as e:
            if str(e.__str__()).find("Zakonczony przez klienta") != -1:
                print(self.addr, "CLOSED: ", e)
                return
            print(self.addr, "ERROR:", e)
            print(self.addr, "CLOSED:")


if __name__ == "__main__":
    s = Server("localhost", 125, ClientThread, fun)
    s.run()
