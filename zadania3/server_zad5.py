from socket import *
import operator

s = socket(AF_INET, SOCK_DGRAM)
s.bind(("127.0.0.1", 12645))

while True:
    message, conn = s.recvfrom(1024)
    try:
        message = gethostbyaddr(message.decode("utf-8"))
    except:
        s.sendto(b"Address is not correct!!!", conn)
    else:
        s.sendto(message[0].encode("utf-8"), conn)
