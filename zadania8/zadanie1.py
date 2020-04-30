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
            rec = socket.recv(1)
            if rec == b"":
                return mes
            mes += rec
    except timeout:
        return mes


socket = socket(AF_INET, SOCK_STREAM)
socket.settimeout(1)
socket.connect((gethostbyname("httpbin.org"), 80))
# socket.connect(("127.0.0.2", 12636))

socket.sendall(b"GET /html HTTP/1.1\r\n"
               b"HOST: 212.182.24.27\r\n"
               b"User-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) "
               b"Version/7.0.3 Safari/7046A194A\r\n\r\n")

recheaders(socket)
body = recvbody(socket)
print(body)
f = open("new.html", "w")
f.write(body.decode("utf-8"))
