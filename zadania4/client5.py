from socket import socket, AF_INET, SOCK_DGRAM, timeout

socket = socket(AF_INET, SOCK_DGRAM)
socket.settimeout(1)
socket.sendto(b"zad14odp;src;60788;dst;2901;data;programming in python is fun", ("localhost", 2019))
print(socket.recv(1024))
socket.sendto(b"zad14odp;src;60788;dst;2901;data;programmig in python is fun", ("localhost", 2019))
print(socket.recv(1024))
socket.sendto(b"zad14odp;src;60788;dst;2901;dta;programming in python is fun", ("localhost", 2019))
print(socket.recv(1024))

