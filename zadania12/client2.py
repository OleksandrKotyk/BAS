from socket import AF_INET, SOCK_STREAM, socket

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(("localhost", 125))
socket.settimeout(10)
print(socket.recv(1024))

socket.sendall("weather\r\nweather\r\n".encode("utf-8") + b"")
print(socket.recv(1024).decode())
print(socket.recv(1024).decode())
socket.sendall("weather12\r\n".encode("utf-8") + b"")
print(socket.recv(1024).decode())
# print(socket.recv(1024).decode())

while True:
    s = input("Data: ")
    socket.sendall(s.encode("utf-8") + b"\r\n")
    print(socket.recv(1024).decode())
