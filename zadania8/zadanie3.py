from socket import *


def recvall(sock, bite):
    message = b""
    for i in range(bite):
        rec = sock.recv(1)
        message += rec
        if rec == b'' or rec is None:
            raise timeout
        elif len(message) > 1 and message[-2:] == b"\r\n":
            return message


def recheaders(sock, fnd=b""):
    global retValue
    while True:
        mes = recvall(sock, 1024)
        if fnd != b"":
            point = mes.find(fnd)
            if point != -1:
                retValue = mes[point + len(fnd): mes.find(b"\r\n")]
        print(mes)
        if mes == b"\r\n":
            return b""


def recvbody(sock):
    mes = b""
    try:
        while True:
            mes += sock.recv(1)
    except timeout:
        return mes


socket = socket(AF_INET, SOCK_STREAM)
socket.settimeout(0.3)
socket.connect(("212.182.24.27", 16080))

socket.sendall(b"HEAD /image.jpg HTTP/1.1\r\n"
               b"HOST: 212.182.24.27\r\n"
               b"Content-Type: image/jpg\r\n"
               b"Connection: keep-alive\r\n\r\n")
retValue = 0
recheaders(socket, b"Content-Length: ")
print("-----------------------")
Content_Length = 0
try:
    Content_Length = int(retValue)
except ValueError:
    print("No int!!!")
    exit()

fullBody = b""
nowValue = 0
for i in range(1, 4):
    nextVal = (Content_Length % 3 - Content_Length) / 3 * i + (Content_Length % 3) * (i - 3)
    socket.sendall(b"GET /image.jpg HTTP/1.1\r\n"
                   b"HOST: 212.182.24.27\r\n"
                   b"Content-Type: image/jpg\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Range: " + nowValue.__str__().encode("utf-8") + b"-" + str(nextVal).encode("utf-8") + b"\r\n\r\n")
    nowValue = nextVal
    recheaders(socket)
    print("-----------------------")
    body = recvbody(socket)
    fullBody += body

f = open("new.jpg", "wb")
f.write(fullBody)
