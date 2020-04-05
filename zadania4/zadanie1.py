from socket import *

socket = socket(AF_INET, SOCK_DGRAM)

raw = "ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61 6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f 6e 20 69 73 20 66 75 6e"

withoutSpace = raw.replace(" ", "")
hexArr = [int("0x" + i, 16) for i in raw.split(" ")]


toSend = "zad14odp;src;{};dst;{};data;{}"

SourcePort = str(int("0x" + withoutSpace[0:4], 16))
DestinationPort = str(int("0x" + withoutSpace[4:8], 16))
data = "".join([chr(i) for i in hexArr[8:]])

toSend = toSend.format(SourcePort, DestinationPort, data)

socket.sendto(toSend.encode("utf-8"),
              ("212.182.24.27 ", 2920))
print(socket.recv(1024))
