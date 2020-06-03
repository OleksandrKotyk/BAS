import socket

from zadania13.materials.functions import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("217.74.64.236", 465))
sock = connect(sock, "poczta.interia.pl", "certs/main.crt", ask=True)

sock.write(b"AUTH LOGIN\r\n")
print(recv_all(sock, 1024))
sock.write(b"b2xla3NhbmR0LmtvdHlrQGludGVyaWEucGw=" + b"\r\n")
print(recv_all(sock, 1024))
sock.write(b"TmV3MTIzNCE=" + b"\r\n")
print(recv_all(sock, 1024))
print(recv_all(sock, 1024))

sock.write(b"MAIL FROM: <" + input_user("FROM: ") + b">\r\n")
print(recv_all(sock, 1024))
sock.write(b"RCPT TO: <" + input_user("TO: ") + b">\r\n")
print(recv_all(sock, 1024))
sock.write(b"DATA" + b"\r\n")
print(recv_all(sock, 1024))

f = open("materials/message_format", "r")
mes = f.read().format(input_user("Subject: ", False), input_user("Message: ", False)).encode("utf-8") + b"\r\n.\r\n"
sock.write(mes)
print(recv_all(sock, 1024))

sock.close()
