from socket import *
import datetime

s = socket(AF_INET, SOCK_DGRAM)
s.bind(("127.0.0.1", 12645))

while True:
    m = s.recvfrom(1024)
    s.sendto(m[0], m[1])
