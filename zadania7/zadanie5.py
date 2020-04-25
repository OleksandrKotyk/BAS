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


def recvall_all(sock, bite, find=b""):
    global retMes
    retMes = b""
    while True:
        try:
            mes = recvall(socket, 1024)
            print(mes)
            if mes.find(find) != -1:
                retMes = mes
        except timeout:
            print()
            return retMes


retMes = b""
socket = socket(AF_INET, SOCK_STREAM)
socket.settimeout(0.2)
socket.connect(("212.182.24.27", 16143))
# socket.connect(("127.0.0.2", 12636))
recvall_all(socket, 1024)

socket.send(b"A1 LOGIN student1@pas.umcs.pl student2020\r\n")
recvall_all(socket, 1024)

socket.send(b'A1 SELECT Inbox\r\n')
recvall_all(socket, 1024)

socket.send(b'A1 SEARCH ALL\r\n')
recvall_all(socket, 1024, b"SEARCH")
nums = retMes[retMes.find(b"SEARCH") + 7: retMes.find(b"\r\n")].split(b" ")

if len(nums) > 0 and nums[0]:
    print("Choose: ", end="")
    for i in nums:
        print(str(i.decode("utf-8")), end=" ")
    print()

    while True:
        n = input("Input: ")
        try:
            int(n)
        except ValueError:
            continue
        break

    socket.send(b'A1 STORE ' + n.encode("utf-8") + b' +FLAGS \\Deleted\r\n')
    recvall_all(socket, 1024)
    socket.send(b'A1 EXPUNGE\r\n')
    recvall_all(socket, 1024)

socket.send(b'A1 LOGOUT\r\n')
socket.send(b'A2 CLOSE\r\n')
recvall_all(socket, 1024)
socket.close()

# socket.send(b'A1 FETCH 1:* (FLAGS)\r\n')
# # recvall_all(socket, 1024)
# nums = []
# while True:
#     try:
#         mes = recvall(socket, 1024)
#         if mes.find(b'\\Seen') == -1 and mes.find(b"A1 OK Fetch completed") == -1:
#             mesNum = mes.split(b" ")[1]
#             nums.append(mesNum)
#         mes = recvall(socket, 1024)
#     except timeout:
#         print()
#         break
#
# print(nums)
# for mesNum in nums:
#     socket.send(b'A1 FETCH ' + mesNum + b' BODY[]\r\n')
#     recvall_all(socket, 1024)
#     socket.send(b'A1 STORE ' + mesNum + b':* +FLAGS \\Seen\r\n')
#     recvall_all(socket, 1024)

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
