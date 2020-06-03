from socket import *
from base64 import *


def recvall(sock, bite):
    mes = b""
    for i in range(bite):
        rec = sock.recv(1)
        if rec == b"\r" and sock.recv(1) == b"\n":
            break
        mes += rec
    return mes

def prep(sock):
    socket.send(b"MAIL FROM: <oleksandt.kotyk@interia.pl>" + b"\r\n")
    print(recvall(sock, 1024))
    socket.send(b"RCPT TO: <malkit2000ll@gmail.com>" + b"\r\n")
    print(recvall(sock, 1024))
    socket.send(b"DATA" + b"\r\n")
    print(recvall(sock, 1024))


socket = socket(AF_INET, SOCK_STREAM)
socket.settimeout(4)
conmes = socket.connect_ex(("217.74.64.236", 587))
print(recvall(socket, 1024))
socket.settimeout(10)

socket.send(b"HELO kasula\r\n")
print(recvall(socket, 1024))
socket.send(b"AUTH LOGIN\r\n")
print(recvall(socket, 1024))
socket.send(b"b2xla3NhbmR0LmtvdHlrQGludGVyaWEucGw=" + b"\r\n")
print(recvall(socket, 1024))
socket.send(b"TmV3MTIzNCE=" + b"\r\n")
print(recvall(socket, 1024))

prep(socket)
f = open("message6.txt", "r")
mes = f.read().encode("utf-8") + b"\r\n.\r\n"
socket.sendall(mes)
ret = recvall(socket, 1024)
print(ret)

prep(socket)
f = open("message7.txt", "r")
mes = f.read().encode("utf-8") + b"\r\n.\r\n"
socket.sendall(mes)
ret = recvall(socket, 1024)
print(ret)

prep(socket)
f = open("message8.txt", "r")
mes = f.read().encode("utf-8") + b"\r\n.\r\n"
socket.sendall(mes)
ret = recvall(socket, 1024)
print(ret)

prep(socket)
f = open("message9.txt", "r")
mes = f.read().encode("utf-8") + b"\r\n.\r\n"
socket.sendall(mes)
ret = recvall(socket, 1024)
print(ret)


