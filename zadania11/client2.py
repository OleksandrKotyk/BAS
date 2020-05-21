from socket import AF_INET, SOCK_STREAM, socket

# TEN SAM CO client.py

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(("localhost", 125))
socket.settimeout(10)
print(socket.recv(1024))
while True:
    s = input("Data: ")
    socket.sendall(s.encode("utf-8"))
    print(socket.recv(1024).decode())
