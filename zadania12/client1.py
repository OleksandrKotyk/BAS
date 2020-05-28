from socket import AF_INET, SOCK_STREAM, socket

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(("localhost", 125))
socket.settimeout(10)
print(socket.recv(1024))
while True:
    s = input("Data: ")
    socket.sendall(s.encode("utf-8") + b"\r\n")
    print(socket.recv(1024).decode())
