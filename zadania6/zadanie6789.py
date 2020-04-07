from socket import *
import time


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

#socket.connect(("217.74.64.236", 110))
#socket.connect(("127.0.0.2", 12636))

socket.connect(("212.182.24.27", 16110))
print(recvall(socket, 1024), end="\n\n")

socket.send(b"USER student2@pas.umcs.pl\r\n")
print(recvall(socket, 1024), end="\n\n")
socket.send(b"PASS student2020\r\n")
print(recvall(socket, 1024), end="\n\n")

#socket.send(b"USER oleksandt.kotyk@interia.pl\r\n")
#print(recvall(socket, 1024))
#socket.send(b"PASS suvzan-gugkyw-veddA2\r\n")
#print(recvall(socket, 1024))


socket.sendall(b"LIST\r\n")
print(recvall(socket, 1024), end="\n\n")

sumOfBytes = 0
theHeist = [-1, -1]
num = b'0'

message = recvall(socket, 1024)
while message != b'.\r\n':
    print(message)
    nBytes, num = int(message[message.find(b" "):].decode("utf-8")), message[:message.find(b" ")]
    sumOfBytes += nBytes
    if nBytes > theHeist[1]:
        theHeist = [num, nBytes]
    message = recvall(socket, 1024)
print()


print("numberOfLetters:", num.decode("utf-8"))
print("sumOfBytes:", sumOfBytes)

if theHeist[0] == -1:
    exit()
socket.sendall(b"RETR " + theHeist[0] + b"\r\n")
message = recvall(socket, 1024)
while message != b'.\r\n':
    print(message)
    message = recvall(socket, 1024)

socket.send(b"QUIT\r\n")
print(recvall(socket, 1024))
socket.close()