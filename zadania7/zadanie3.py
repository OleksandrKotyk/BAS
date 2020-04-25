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


def recvall_all(sock, bite, find=b"", prt=True):
    global retMes
    retMes = b""
    while True:
        try:
            mes = recvall(socket, 1024)
            if prt:
                print(mes)
            if mes.find(find) != -1:
                retMes = mes
        except timeout:
            if prt:
                print()
            return retMes


retMes = b""
socket = socket(AF_INET, SOCK_STREAM)
socket.settimeout(0.2)

# socket.connect(("212.182.24.27", 16143))
socket.connect(("127.0.0.2", 12636))
recvall_all(socket, 1024)

socket.send(b"A1 LOGIN student1@pas.umcs.pl student2020\r\n")
recvall_all(socket, 1024)

socket.send(b'A1 LIST "" *\r\n')
res = 0
boxes = []
try:
    message = recvall(socket, 1024)
    while message.find(b"LIST") != -1:
        boxes.append(message[message.find(b'"/"') + 3:message.find(b"\r\n")])
        message = recvall(socket, 1024)
except timeout:
    var = None

for box in boxes:
    socket.send(b'A1 STATUS' + box + b' (MESSAGES)\r\n')
    recvall_all(socket, 1024, b"MESSAGES", False)
    res += int(retMes.split(b" ")[4].replace(b")\r\n", b""))
print(boxes)
print("Number:", res)

socket.send(b'A1 LOGOUT\r\n')
socket.send(b'A2 CLOSE\r\n')
recvall_all(socket, 1024)
socket.close()

# print("Inbox: ", int(retMes.split(b" ")[1]))


# socket.send(b'A1 SEARCH ALL\r\n')
# recvall_all(socket, 1024)
#
# socket.send(b'A1 FETCH 1 BODY[]\r\n')
# recvall_all(socket, 1024)

# socket.send(b"PASS student2020\r\n")
# print(recvall(socket, 1024), end="\n\n")

# socket.send(b"USER oleksandt.kotyk@interia.pl\r\n")
# print(recvall(socket, 1024))
# socket.send(b"PASS suvzan-gugkyw-veddA2\r\n")
# print(recvall(socket, 1024))
