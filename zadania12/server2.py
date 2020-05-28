import json
from queue import Queue, Empty
from select import select
from socket import AF_INET, SOCK_STREAM, timeout, gethostbyname, error
from socket import socket as sock


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
            rec = sock.recv(1)
            if rec == b"":
                return mes
            mes += rec
    except timeout:
        return mes


buf_size = 1024

socket = sock(AF_INET, SOCK_STREAM)
socket.setblocking(False)
socket.bind(("localhost", 125))
socket.listen(10)

inputs = [socket]
outputs = []

message_queues = {}
rec_buffer = {}

socket_weather = sock(AF_INET, SOCK_STREAM)
socket_weather.settimeout(0.5)
socket_weather.connect((gethostbyname("api.openweathermap.org"), 80))

while inputs:
    readable, writable, exceptional = select(inputs, outputs, inputs)
    for s in readable:
        if s is socket:
            conn, addr = s.accept()
            print("Conected:", conn)
            conn.setblocking(0)
            conn.sendall(b"Hello")
            inputs.append(conn)
            message_queues[conn] = Queue()
            rec_buffer[conn] = b""
        else:
            try:
                data = s.recv(buf_size)
            except error:
                if s in outputs:
                    outputs.remove(s)

                inputs.remove(s)
                s.close()
                del message_queues[s]
                print("delete because of exception")
                continue
            print(s.getsockname(), ":", data)
            if data:
                rec_buffer[s] += data

                splt = rec_buffer[s].split(b"\r\n")

                rec_buffer[s] = splt[-1]

                for i in splt[:-1]:
                    if i == b"weather":
                        try:
                            socket_weather.sendall(
                                b"GET /data/2.5/weather?appid=d4af3e33095b8c43f1a6815954face64&id=765876 HTTP/1.1\r\n"
                                b"HOST: " + gethostbyname("api.openweathermap.org").encode() + b"\r\n\r\n")
                        except error:
                            socket_weather = sock(AF_INET, SOCK_STREAM)
                            socket_weather.settimeout(0.5)
                            socket_weather.connect((gethostbyname("api.openweathermap.org"), 80))
                            socket_weather.sendall(
                                b"GET /data/2.5/weather?appid=d4af3e33095b8c43f1a6815954face64&id=765876 HTTP/1.1\r\n"
                                b"HOST: " + gethostbyname("api.openweathermap.org").encode() + b"\r\n\r\n")
                        recheaders(socket_weather)
                        body = recvbody(socket_weather)
                        body_dict = json.loads(body)
                        print(body)
                        message_queues[s].put(json.dumps(body_dict, indent=4, sort_keys=True).encode() + b"\r\n")
                    else:
                        message_queues[s].put(b"No proper comand\r\n")

                if s not in outputs:
                    outputs.append(s)
            else:
                if s in outputs:
                    outputs.remove(s)

                inputs.remove(s)
                s.close()
                del message_queues[s]
                print("delete")

    for s in writable:
        try:
            mes = message_queues[s].get_nowait()
        except Empty:
            print("Empty")
            outputs.remove(s)
        else:
            print("send_to :", s.getsockname(), "::", mes)
            s.sendall(mes)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
