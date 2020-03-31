from socket import *

s = socket(AF_INET, SOCK_DGRAM)

s.settimeout(15)
for j in range(4):
    m = input("Your IpAddress: ")
    s.sendto(m.encode("utf-8"), ("127.0.0.1", 12645))
    m = s.recvfrom(1024)
    print("Your result: ", m[0].decode("utf-8"))
