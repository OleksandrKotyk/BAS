from socket import *


def recvall(sock, bite):
    mes = b""
    for i in range(bite):
        rec = sock.recv(1)
        mes += rec
        if rec == b'' or rec is None:
            raise timeout
        elif len(mes) > 1 and mes[-2:] == b"\r\n":
            return mes


def recheaders(sock):
    while True:
        mes = recvall(sock, 1024)
        print(mes)
        if mes == b"\r\n":
            return


def recvbody(sock):
    mes = b""
    try:
        while True:
            mes += sock.recv(1)
    except timeout:
        return mes


def makeFrame(text, frm):
    for i in text:
        frm.append(i)


def receveWS(sock):
    while True:
        MASK = sock.recv(1)
        print(MASK)


socket = socket(AF_INET, SOCK_STREAM)
socket.connect((gethostbyname("echo.websocket.org"), 80))
# socket.connect(("127.0.0.2", 12636))
print((gethostbyname("websocket.org")))
socket.settimeout(3)

socket.sendall(b'GET ws://echo.websocket.org HTTP/1.1\r\n'
               b'Host: echo.websocket.org\r\n'
               b'Upgrade: websocket\r\n'
               b'Connection: Upgrade\r\n'
               b'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n'
               b'Origin: http://websocket.org\r\n'
               b'Sec-WebSocket-Protocol: chat\r\n'
               b'Sec-WebSocket-Version: 13\r\n\r\n'
               )
recheaders(socket)

socket.close()
