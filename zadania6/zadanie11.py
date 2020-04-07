import base64
from socket import *


def recvall(sock, bite):
    mes = b""
    for i in range(bite):
        rec = sock.recv(1)
        mes += rec
        if rec == b"":
            raise timeout
        elif len(mes) > 1 and mes[-2:] == b"\r\n":
            return mes


socket = socket(AF_INET, SOCK_STREAM)
socket.settimeout(4)

# socket.connect(("217.74.64.236", 110))
socket.connect(("212.182.24.27", 16110))
# socket.connect(("127.0.0.2", 12636))
print(recvall(socket, 1024))

# socket.send(b"USER oleksandt.kotyk@interia.pl\r\n")
# print(recvall(socket, 1024))
#
# socket.send(b"PASS suvzan-gugkyw-veddA2\r\n")
# print(recvall(socket, 1024))


socket.send(b"USER student2@pas.umcs.pl\r\n")
print(recvall(socket, 1024), end="\n")
socket.send(b"PASS student2020\r\n")
print(recvall(socket, 1024), end="\n")

num = 0

socket.sendall(b"LIST\r\n")
recvall(socket, 1024)
message = recvall(socket, 1024)
while message != b'.\r\n':
    nBytes, num = int(message[message.find(b" "):].decode("utf-8")), message[:message.find(b" ")]
    message = recvall(socket, 1024)

img = b""
filename = b""

print(num)

for i in range(1, int(num) + 1):
    socket.send(b"RETR " + str(i).encode("utf-8") + b"\r\n")
    message = recvall(socket, 1024)
    while message != b'.\r\n':
        if message.find(b'Content-Type: image/jpeg') != -1 or message.find(b'Content-Type: image/png') != -1:
            while message != b'\r\n' and message != b'.\r\n':
                if message.find(b"name=") != -1:
                    if message.find(b'name="') != -1:
                        beg = message.find(b'"')
                        end = message.find(b'"', beg + 1)
                    else:
                        beg = message.find(b"name=") + 4
                        end = message.find(b';\r\n', beg + 5)
                    filename = message[beg + 1: end]
                    filename = filename.replace(b"name=", b"")
                    filename = filename.replace(b"\r", b"")
                message = recvall(socket, 1024)
            message = recvall(socket, 1024)
            while message.find(b"--") == -1:
                img += message[:message.find(b"\r\n")]
                message = recvall(socket, 1024)
            if filename != b"":
                img = base64.decodebytes(img)
                op = open(filename.decode("utf-8"), "wb")
                op.write(img)
        message = recvall(socket, 1024)

print(filename)
socket.send(b"QUIT\r\n")
print(recvall(socket, 1024))
socket.close()
