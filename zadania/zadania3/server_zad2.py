from socket import *
import datetime

s = socket(AF_INET, SOCK_STREAM)
s.bind(("127.0.0.1", 12645))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr[0], ":", addr[1], sep="")
    m = conn.recv(1024)
    conn.send(m)
