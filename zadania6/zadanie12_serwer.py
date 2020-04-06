import socket


def next_mes(sock):
    ret_mes = b""
    while True:
        c = sock.recv(1)
        ret_mes += c
        if c == b"":
            raise socket.timeout
        if len(ret_mes) > 1 and ret_mes[-2:] == b'\r\n':
            return ret_mes


emails = [open("email", "rb"), open("email_with_img", "rb")]
sizes = [b'1 3418\r\n', b'2 26740\r\n']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.2", 12636))
s.listen(5)

while True:
    conn, addr = s.accept()
    conn.sendall(b"+OK 12e1d8efc92aef4\r\n")
    print("Connected to:", addr)
    while True:
        try:
            mes = next_mes(conn)
            if mes.find(b"USER ") != -1:
                conn.sendall(b'+OK Tell me your password.\r\n')
                mes = next_mes(conn)
                if mes.find(b"PASS ") != -1:
                    conn.sendall(b'+OK Welcome aboard! You have 2 message.\r\n')
                else:
                    conn.sendall(b'-ERR The command sent is invalid or unimplemented.\r\n')
            elif mes.find(b"LIST\r\n") != -1:
                conn.sendall(b'+OK Scan list follows:\r\n')
                for i in sizes:
                    conn.sendall(i)
                conn.sendall(b'.\r\n')
            elif mes.find(b"RETR ") != -1:
                n = mes[mes.find(b" ") + 1:].replace(b"\r\n", b"")
                n = int(n)
                n -= 1
                emails[n]
                conn.sendall(b'+OK Message follows\r\n')
                for i in emails[n]:
                    conn.sendall(i)
                conn.sendall(b'.\r\n')
                emails[n].seek(0, 0)
            else:
                conn.sendall(b'-ERR The command sent is invalid or unimplemented.\r\n')
        except socket.timeout:
            break
        except ConnectionResetError:
            conn.sendall(b'-ERR The command sent is invalid or unimplemented.\r\n')
        except IndexError:
            conn.sendall(b'-ERR The command sent is invalid or unimplemented.\r\n')
    print("Connection is close!!!", addr)