from socket import *
import time
import base64


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

socket.connect(("217.74.64.236", 110))
# socket.connect(("127.0.0.2", 12636))
print(recvall(socket, 1024))

socket.send(b"USER oleksandt.kotyk@interia.pl\r\n")
print(recvall(socket, 1024))

socket.send(b"PASS suvzan-gugkyw-veddA2\r\n")
print(recvall(socket, 1024))

num = 0

socket.sendall(b"LIST\r\n")
recvall(socket, 1024)
message = recvall(socket, 1024)
while message != b'.\r\n':
    nBytes, num = int(message[message.find(b" "):].decode("utf-8")), message[:message.find(b" ")]
    message = recvall(socket, 1024)

print(num)
img = b""
filename = b""

for i in range(1, int(num) + 1):
    socket.send(b"RETR " + str(i).encode("utf-8") + b"\r\n")
    message = recvall(socket, 1024)
    while message != b'.\r\n':
        if message.find(b'Content-Type: image/png') != -1:
            while message != b'\r\n' and message != b'.\r\n':
                if message.find(b" name") != -1:
                    beg = message.find(b'"')
                    end = message.find(b'"', beg + 1)
                    filename = message[beg + 1: end]
                message = recvall(socket, 1024)
            message = recvall(socket, 1024)
            while message.find(b"--") == -1:
                img += message[:message.find(b"\r\n")]
                message = recvall(socket, 1024)
            if filename != b"":
                img = base64.decodebytes(img)
                op = open(filename.decode("utf-8"), "wb")
                op.write(img)
            exit()
        message = recvall(socket, 1024)




