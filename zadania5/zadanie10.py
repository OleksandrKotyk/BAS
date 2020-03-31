import socket

mesMap = dict()


def message(m, c):
    while True:
        f = m.find(b"\r\n")
        if f != -1:
            return f, m
        rec = c.recv(1)
        if not rec:
            return 2, mes
        m += rec


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.2", 12636))
s.listen(5)

while True:
    conn, addr = s.accept()
    conn.send(b"Hello\r\n")
    mes = b""
    ch = False
    while True:
        conn.settimeout(1)
        try:
            fnd, mes = message(mes, conn)
        except socket.timeout:
            break
        cStr = mes[:fnd]
        if len(cStr) == 0:
            break
        print(cStr)
        mes = mes[fnd + 2:]

        if cStr.find(b"HELO ") == 0:
            conn.send(b'250 poczta.interia.pl\r\n')
        elif cStr.find(b"AUTH LOGIN ") == 0:
            conn.send(b'334 VXNlcm5hbWU6\r\n')
            try:
                fnd, mes = message(mes, conn)
            except socket.timeout:
                break
            mes = mes[fnd + 2:]
            conn.send(b'334 UGFzc3dvcmQ6\r\n')
            try:
                fnd, mes = message(mes, conn)
            except socket.timeout:
                break
            mes = mes[fnd + 2:]
            conn.send(b'235 2.7.0 Authentication successful\r\n')
        elif cStr.find(b"MAIL FROM:") == 0:
            conn.send(b'250 2.1.5 Ok\r\n')
        elif cStr.find(b"RCPT TO:") == 0:
            conn.send(b'250 2.1.5 Ok\r\n')
        elif cStr.find(b"DATA") == 0:
            conn.send(b'354 End data with <CR><LF>.<CR><LF>\r\n')
        else:
            conn.send(b"Bad message!!!\r\n")
