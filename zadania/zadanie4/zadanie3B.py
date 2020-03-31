from socket import *

socket = socket(AF_INET, SOCK_DGRAM)

raw = "45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b " \
      "c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1 " \
      "80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01 " \
      "00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67 " \
      "72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e"

withoutSpace = raw.replace(" ", "")
hexArr = [int("0x" + i, 16) for i in raw.split(" ")]

toSend = "zad15odpB;srcport;{};dstport;{};data;{}"

SourcePort = str(int("0x" + withoutSpace[40:44], 16))
DestinationPort = str(int("0x" + withoutSpace[44:48], 16))
data = "".join([chr(i) for i in hexArr[52:]])

toSend = toSend.format(SourcePort, DestinationPort, data)

socket.sendto(toSend.encode("utf-8"), ("212.182.24.27 ", 2923))
print(socket.recv(1024))
