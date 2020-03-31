from socket import *

s = socket(AF_INET, SOCK_DGRAM)

s.settimeout(1)
m = input("Your message: ")
s.sendto(m.encode("utf-8"), ("127.0.0.1", 12645))
m = s.recvfrom(1024)
print("From: ", m[0].decode("utf-8"))
