from socket import *
import time
import math

class NotProperMess(Exception):
    pass


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
    headers = []
    while True:
        mes = recvall(sock, 1024)
        if mes == b"\r\n":
            return headers
        headers.append(mes)


def recvbody(sock):
    mes = b""
    try:
        while True:
            mes += sock.recv(1)
    except timeout:
        return mes


def makeFrame(text, frm):
    for i in text:
        frm.append(i)


def receveWS(sock):
    fir = int.from_bytes(sock.recv(1), byteorder="big")
    sec = int.from_bytes(sock.recv(1), byteorder="big")
    if sec == 126:
        sec = int.from_bytes(sock.recv(2), byteorder="big")
    elif sec == 127:
        sec = int.from_bytes(sock.recv(8), byteorder="big")
    else:
        raise NotProperMess

    retmes = b""
    for i in range(sec):
        retmes += sock.recv(1)
    return retmes


reqHeaders = [b'HTTP/1.1 101 Web Socket Protocol Handshake\r\n',
              b'Access-Control-Allow-Credentials: true\r\n',
              b'Access-Control-Allow-Headers: content-type\r\n',
              b'Access-Control-Allow-Headers: authorization\r\n',
              b'Access-Control-Allow-Headers: x-websocket-extensions\r\n',
              b'Access-Control-Allow-Headers: x-websocket-version\r\n',
              b'Access-Control-Allow-Headers: x-websocket-protocol\r\n',
              b'Access-Control-Allow-Origin: http://websocket.org\r\n',
              b'Connection: Upgrade\r\n',
              b'Date: Sat, 09 May 2020 20:11:37 GMT\r\n',
              b'Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=\r\n',
              b'Server: Kaazing Gateway\r\n',
              b'Upgrade: websocket\r\n',
              b'\r\n']

goodHeaders = [b'GET ws://echo.websocket.org HTTP/1.1\r\n',
               b'Host: echo.websocket.org\r\n',
               b'Upgrade: websocket\r\n',
               b'Connection: Upgrade\r\n',
               b'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n',
               b'Origin: http://websocket.org\r\n',
               b'Sec-WebSocket-Protocol: chat\r\n',
               b'Sec-WebSocket-Version: 13\r\n']

s = socket(AF_INET, SOCK_STREAM)
s.bind(("127.0.0.2", 12636))
s.listen(1)

while True:
    conn, addr = s.accept()
    conn.settimeout(20)
    print("Connected to:", addr)
    chatOn = False
    full = b""
    while True:
        try:
            if not chatOn:
                mes = recheaders(conn)
                if mes == goodHeaders:
                    conn.sendall(b"".join(reqHeaders))
                chatOn = True
            else:
                mes = conn.recv(1)
                if mes == b"":
                    timeout("is closed")
                full += mes
                if len(full) >= 2 and full[0] == int("81", 16):
                    # print(full)
                    sec = full[1]
                    if sec == 126:
                        if len(full) >= 4:
                            sec = int.from_bytes(full[2:4], byteorder="big")
                            if len(full[4:]) == sec and sec != 0:
                                conn.sendall(full)
                                full = b""
                    elif sec == 127:
                        if len(full) >= 10:
                            sec = int.from_bytes(full[2:10], byteorder="big")
                            if len(full[10:]) == sec and sec != 0:
                                conn.sendall(full)
                                full = b""
                    elif sec > 125:
                        full = b""
                        conn.sendall(b'\x03\xea')
                    else:
                        if len(full[2:]) == sec and sec != 0:
                            conn.sendall(full)
                            full = b""
                elif len(full) > 0 and full[0] == int("88", 16):
                    raise timeout("opcode - 8")


        except (timeout, ConnectionResetError, ConnectionAbortedError) as e:
            print("Error:", e)
            break
    conn.close()
    print("Connection is closed!!!", addr)
