from socket import *

socket = socket(AF_INET, SOCK_DGRAM)
socket.bind(("localhost", 2019))

while True:
    rec = socket.recvfrom(1024)
    mustbe = b"zad14odp;src;60788;dst;2901;data;programming in python is fun"

    mbArr = mustbe.decode("utf-8").split(";")
    rARR = rec[0].decode("utf-8").split(";")

    if rec[0] == mustbe:
        socket.sendto(b"TAK", rec[1])
    elif rARR[0] == mbArr[0] and rARR[1] == mbArr[1] and rARR[3] == mbArr[3] and rARR[5] == mbArr[5]:
        socket.sendto(b"NIE", rec[1])
    else:
        socket.sendto(b"BADSYNTAX", rec[1])
