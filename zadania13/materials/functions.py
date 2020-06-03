import ssl
from socket import timeout, error


def recv_all(conn, bite):
    text = b""
    for i in range(bite):
        rec = conn.recv(1)
        if not rec:
            raise error
        text += rec
        if len(text) >= 2 and text[-2:] == b"\r\n":
            break
    return text


def input_user(ask_for="", code=True):
    inp = ""
    while not inp:
        inp = input(ask_for)
    return inp.encode("utf-8") if code else inp


def connect(conn, server_name=None, ca_cert="", cert="", key="", ask=False):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ver = ""
    if ask:
        ver = input_user("Verify = 'y', not verify = something else: ", False)
        ver = "" if ver == "y" else ver
    if ca_cert and not ver:
        print("\033[3;36mZ żądaniem!", sep="")
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(ca_cert)
        if key and cert:
            context.load_cert_chain(certfile=cert, keyfile=key)
    else:
        print("\033[3;35mBez żądania!", sep="")

    conn = context.wrap_socket(conn) if not ssl.HAS_SNI or not server_name \
        else context.wrap_socket(conn, server_hostname=server_name)

    if ca_cert and not ver:
        ca_cert = conn.getpeercert()
        print(ca_cert)
        if not ca_cert or ssl.match_hostname(ca_cert, server_name):
            raise Exception("Cert_Error")
    return conn


def reach_headers(sock, fnd=b"", print_headers=True):
    while True:
        mes = recv_all(sock, 1024)
        if fnd != b"":
            point = mes.find(fnd)
            if point != -1:
                fnd = mes[point + len(fnd): mes.find(b"\r\n")]
        if print_headers:
            print(mes)
        if mes == b"\r\n":
            return fnd


def recv_body(sock, length):
    mes = b""
    try:
        for i in range(length):
            mes += sock.recv(1)
        return mes
    except timeout:
        return mes


# server

def rec_messages(connection):
    addr = ""
    try:
        addr = connection.getpeername()
        while True:
            mes = recv_all(connection, 4096)
            print(addr, mes, sep=": ")
            connection.sendall(mes)
    except error:
        print("Disconnected : {}".format(addr[0] + ":" + str(addr[1])))
        exit(0)
