from socket import *

s = socket(AF_INET, SOCK_STREAM)

s.settimeout(1)
s.connect(("127.0.0.1", 12645))
m = input("Your message: ")
s.send(m.encode("utf-8"))
m = s.recv(1024)
print("From: ", m.decode("utf-8"))
