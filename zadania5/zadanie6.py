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


socket = socket(AF_INET, SOCK_STREAM)
socket.settimeout(4)
conmes = socket.connect_ex(("217.74.64.236", 587))
ret = recvall(socket, 1024)
print(ret)

socket.send(b"HELO kasula\r\n")
ret = recvall(socket, 1024)
print(ret)

socket.send(b"AUTH LOGIN\r\n")
ret = recvall(socket, 1024)
print(ret)

socket.send(b64encode(b"ts.geoinf@interia.eu") + b"\r\n")
ret = recvall(socket, 1024)
print(ret)

socket.send(b64encode(b"student2020") + b"\r\n")
ret = recvall(socket, 1024)
print(ret)

socket.send(b"MAIL FROM: <ts.geoinf@interia.eu>" + b"\r\n")
ret = recvall(socket, 1024)
print(ret)

socket.send(b"RCPT TO: <malkit2000ll@gmail.com>" + b"\r\n")
ret = recvall(socket, 1024)
print(ret)

socket.send(b"DATA" + b"\r\n")
ret = recvall(socket, 1024)
print(ret)

# socket.send(b"From: Nathaniel Borenstein <nsb@bellcore.com>\n"
#             b"Subject: Sample message\n"
#             b"MIME-Version: 1.0\n"
#             b"Content-Type: multipart/mixed; boundary=sep\n"
#             b"--sep"
#             b"Tojesttresc wiadomosci--sep--" + b"\r\n")
# ret = recvall(socket, 1024)
# print(ret)
