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


emails = {b"1 3418", }

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
            if mes.find(b"USER oleksandt.kotyk@interia.pl\r\n") != -1:
                conn.sendall(b'+OK Tell me your password.\r\n')
                mes = next_mes(conn)
                if mes.find(b"PASS suvzan-gugkyw-veddA2\r\n") != -1:
                    conn.sendall(b'+OK Welcome aboard! You have 1 message.\r\n')
                else:
                    conn.sendall(b'-ERR The command sent is invalid or unimplemented.\r\n')
            elif mes.find(b"LIST\r\n") != -1:
                conn.sendall(b'+OK Scan list follows:\r\n')
                conn.sendall(b'1 3418\r\n')
                conn.sendall(b'.\r\n')
            elif mes.find(b"RETR 1") != -1:
                conn.sendall(b'+OK Message follows\r\n')
                for i in open("email", "r"):
                    conn.sendall(i.encode("utf-8") + b'\r\n')
                conn.sendall(b'.\r\n')
            else:
                conn.sendall(b'-ERR The command sent is invalid or unimplemented.\r\n')
        except socket.timeout:
            break
    print("Connection is closed!!!", addr)