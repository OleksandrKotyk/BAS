from socket import *


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
    heads_array = []
    while True:
        mes = recvall(sock, 1024)
        if mes == b"\r\n":
            return heads_array
        heads_array.append(mes.replace(b"\r\n", b""))


def recvbody(sock):
    m = b""
    try:
        while True:
            m += sock.recv(1)
    except timeout:
        return m


pages = {b"/error": open("error.html", "rb"), b"/html": open("head.html", "rb")}

s = socket(AF_INET, SOCK_STREAM)
s.bind(("127.0.0.2", 12636))
s.listen(1)

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    while True:
        try:
            heads_ar = recheaders(conn)
            print(heads_ar)
            first = heads_ar.pop(0)
            ar_first = first.split(b" ")
            print(ar_first)
            if ar_first[0] not in [b"GET", b"HEAD"]:
                conn.sendall(b'HTTP/1.1 400 Bad Request\r\n'
                             b'Date: Thu, 30 Apr 2020 16:43:23 GMT\r\n'
                             b'Content-Type: text/html\r\n'
                             b'Content-Length: 183\r\n'
                             b'Connection: keep-alive\r\n'
                             b'\r\n'
                             b'<html>\n  <head>\n    <title>Bad Request</title>\n  </head>\n  <body>\n'
                             b'    <h1><p>Bad Request</p></h1>\n'
                             b'    Invalid Method &#x27;Invalid HTTP method: &#x27;GT&#x27;&#x27;\n'
                             b'  </body>\n</html>\n')
                break
            if ar_first[1] not in [b"/error", b"/html"]:
                print(ar_first[1])
                conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n'
                             b'Date: Thu, 30 Apr 2020 16:49:14 GMT\r\n'
                             b'Content-Type: text/html\r\n'
                             b'Content-Length: 233\r\n'
                             b'Connection: keep-alive\r\n'
                             b'Server: gunicorn/19.9.0\r\n'
                             b'Access-Control-Allow-Origin: *\r\n'
                             b'Access-Control-Allow-Credentials: true\r\n'
                             b'\r\n')
                conn.sendall(b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                             b'<title>404 Not Found</title>\n'
                             b'<h1>Not Found</h1>\n'
                             b'<p>The requested URL was not found on the server. '
                             b' If you entered the URL manually please check your spelling and try again.</p>\n')
                break
            if ar_first[2] != b"HTTP/1.1":
                raise timeout
            for head in heads_ar:
                spt = head.split(b" ")
                if spt[0] not in [b"HOST:", b"User-agent:", b"Version:", b"Content-Type:", b"Connection:", b"Range:",
                                  b"Content-Length:"]:
                    print(spt[0])
                    conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n'
                                 b'Date: Thu, 30 Apr 2020 16:49:14 GMT\r\n'
                                 b'Content-Type: text/html\r\n'
                                 b'Content-Length: 233\r\n'
                                 b'Connection: keep-alive\r\n'
                                 b'Server: gunicorn/19.9.0\r\n'
                                 b'Access-Control-Allow-Origin: *\r\n'
                                 b'Access-Control-Allow-Credentials: true\r\n'
                                 b'\r\n')
                    conn.sendall(b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                                 b'<title>404 Not Found</title>\n'
                                 b'<h1>Not Found</h1>\n'
                                 b'<p>The requested URL was not found on the server. '
                                 b' If you entered the URL manually please check your spelling and try again.</p>\n')
                    break

            conn.sendall(b'HTTP/1.1 200 OK\r\n'
                         b'Date: Thu, 30 Apr 2020 17:27:21 GMT\r\n'
                         b'Content-Type: text/html; charset=utf-8\r\n'
                         b'Content-Length: 3741\r\n'
                         b'Connection: keep-alive\r\n'
                         b'Server: gunicorn/19.9.0\r\n'
                         b'Access-Control-Allow-Origin: *\r\n'
                         b'Access-Control-Allow-Credentials: true\r\n'
                         b'\r\n')
            conn.sendall(pages[ar_first[1]].read())

        except (timeout, ConnectionResetError, IndexError):
            conn.sendall(b'HTTP/1.1 400 Bad Request\r\n'
                         b'Server: awselb/2.0\r\n'
                         b'Date: Thu, 30 Apr 2020 16:51:47 GMT\r\n'
                         b'Content-Type: text/html\r\n'
                         b'Content-Length: 138\r\n'
                         b'Connection: close\r\n'
                         b'\r\n')
            break
    conn.close()
    print("Connection is closed!!!", addr)
