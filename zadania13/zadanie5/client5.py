import socket

from zadania13.zadanie4.client4 import Client

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("127.0.0.1", 8080))
client = Client(sock, "okotyk.com", "../certs/server.crt", "../certs/client.crt", "../certs/client.key")
client.send_rec_mes(45)
