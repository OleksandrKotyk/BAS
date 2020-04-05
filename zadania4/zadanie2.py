from socket import *

socket = socket(AF_INET, SOCK_DGRAM)

raw = "0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18 00 e3 " \
      "67 71 00 00 01 01 08 0a 02 c1 a4 ee 00 1a 4c ee " \
      "68 65 6c 6c 6f 20 3a 29"

withoutSpace = raw.replace(" ", "")
hexArr = [int("0x" + i, 16) for i in raw.split(" ")]


toSend = "zad13odp;src;{};dst;{};data;{}"

SourcePort = str(int("0x" + withoutSpace[0:4], 16))
DestinationPort = str(int("0x" + withoutSpace[4:8], 16))
data = "".join([chr(i) for i in hexArr[2 + 2 + 4 + 4 + 2 + 2 + 2 + 2 + 12:]])

toSend = toSend.format(SourcePort, DestinationPort, data)

socket.sendto(b"zad13odp;src;2900;dst;35211;data;hello :)",
              ("212.182.24.27 ", 2921))
print(socket.recv(1024))

