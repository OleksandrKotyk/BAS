from socket import *
import operator

s = socket(AF_INET, SOCK_DGRAM)
s.bind(("127.0.0.1", 12645))

while True:
    message, conn = s.recvfrom(1024)
    try:
        message = gethostbyname(message.decode("utf-8"))
    except:
        s.sendto(b"Host is not correct!!!", conn)
    else:
        s.sendto(message.encode("utf-8"), conn)
