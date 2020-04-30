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
            mes += socket.recv(1)
    except timeout:
        return mes


socket = socket(AF_INET, SOCK_STREAM)
socket.settimeout(1)
socket.connect((gethostbyname("httpbin.org"), 80))

socket.sendall(b"POST /post HTTP/1.1\r\n"
               b"HOST: 212.182.24.27\r\n"
               b"Content-Type: application/x-www-form-urlencoded\r\n"
               b"Content-Length: 129\r\n"
               b"\r\n"
               b"custname=sdf&custtel=sadf&custemail=malkit2000ll%40fmail.com&size=small&topping=bacon&topping"
               b"=mushroom&delivery=11%3A15&comments=")

recheaders(socket)
body = recvbody(socket)
f = open("new.png", "wb")
print(body.decode("utf-8"))
