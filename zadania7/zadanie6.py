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


emails = [open("../zadania6/email.eml", "rb"), open("../zadania6/email_with_img.eml", "rb")]
boxes = {b'junk': 1, b'drafts': 2, b'sent': 3, b'trash': 4, b'inbox': 2}
tagboxes = {b'junk': b"\\Junk", b'drafts': b"\\Drafts", b'sent': b"\\Sent", b'trash': b"\\sent", b'inbox': b""}
sizes = [b'1 3418\r\n', b'2 26740\r\n']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.2", 12636))
s.listen(5)

while True:
    login = False
    selected = False
    conn, addr = s.accept()
    conn.sendall(b'* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE STARTTLS AUTH=PLAIN '
                 b'AUTH=LOGIN] Dovecot (Ubuntu) ready.\r\n')
    print("Connected to:", addr)
    while True:
        try:
            mes = next_mes(conn)
            mes = mes.lower()
            print(mes)
            if mes.find(b"a1 login ") != -1:
                if len(mes.split(b" ")) == 4:
                    login = True
                    conn.sendall(b'A1 OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT '
                                 b'SORT=DISPLAY THREAD=REFERENCES THREAD=REFS THREAD=ORDEREDSUBJECT MULTIAPPEND '
                                 b'URL-PARTIAL CATENATE UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 '
                                 b'CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS BINARY '
                                 b'MOVE QUOTA ACL RIGHTS=texk] Logged in\r\n')
                else:
                    break
            elif mes.find(b"a1 status ") != -1 and login and len(mes.split(b" ")) == 4:
                mes = mes.replace(b"\r\n", b"")
                ar = mes.split(b" ")
                print(ar)
                if ar[2] in boxes and ar[3] == b'(messages)':
                    conn.sendall(b'* STATUS ' + ar[2] + b' (MESSAGES ' + str(boxes[ar[2]]).encode("utf-8") + b')\r\n')
                else:
                    break
            elif mes.find(b"close") != -1:
                break
            elif mes.find(b"logout") != -1:
                conn.sendall(b'* BYE Logging out\r\n')
                conn.sendall(b'A1 OK Logout completed (0.001 + 0.000 secs).\r\n')
            elif mes.find(b"a1 select") != -1 and login:
                mes = mes.replace(b"\r\n", b"")
                ar = mes.split(b" ")
                if len(ar) == 3 and ar[2] == b"inbox":
                    conn.sendall(b'* FLAGS (\\Answered \\Flagged \\Deleted \\Seen \\Draft $Forwarded)\r\n')
                    conn.sendall(b'* OK [PERMANENTFLAGS (\\Answered \\Flagged \\Deleted \\Seen \\Draft $Forwarded '
                                 b'\\*)] Flags permitted.\r\n')
                    conn.sendall(b'* 0 EXISTS\r\n')
                    conn.sendall(b'* 0 RECENT\r\n')
                    conn.sendall(b'* OK [UIDVALIDITY 1585998650] UIDs valid\r\n')
                    conn.sendall(b'* OK [UIDNEXT 21] Predicted next UID\r\n')
                    conn.sendall(b'* OK [HIGHESTMODSEQ 131] Highest\r\n')
                    conn.sendall(b'A1 OK [READ-WRITE] Select completed (0.001 + 0.000 secs).\r\n')
                    selected = True
                else:
                    break
            elif mes.find(b'a1 list "" *\r\n') != -1 and login:
                for i in boxes:
                    conn.sendall(b'* LIST (\\HasNoChildren ' + tagboxes[i] + b') "/" ' + i + b'\r\n')
                conn.sendall(b'A1 OK List completed (0.001 + 0.000 secs).\r\n')
            elif mes.find(b'a1 fetch 1:* (flags)\r\n') != -1:
                conn.sendall(b'* 1 FETCH (FLAGS ())\r\n')
                conn.sendall(b'* 2 FETCH (FLAGS ())\r\n')
                conn.sendall(b'A1 OK Fetch completed (0.001 + 0.000 secs).\r\n')
            elif mes.find(b'a1 fetch') != -1 and mes.find(b'body[]') != -1:
                mes = mes.replace(b"\r\n", b"")
                ar = mes.split(b" ")
                try:
                    num = int(ar[2])
                    message = emails[num - 1]
                except ValueError:
                    conn.sendall(b'A1 BAD Error in IMAP command received by server.\r\n')
                    continue
                for i in message:
                    conn.sendall(i + b"\r\n")
                conn.sendall(b'A1 OK Fetch completed (0.001 + 0.000 secs).\r\n')
            elif mes.find(b'a1 store') != -1 and login and selected:
                mes = mes.replace(b"\r\n", b"")
                ar = mes.split(b" ")
                try:
                    num = int(ar[2].replace(b":*", b''))
                except ValueError:
                    conn.sendall(b'A1 BAD Error in IMAP command received by server.\r\n')
                    continue
                conn.sendall(b'A1 OK Store completed (0.001 + 0.000 secs).\r\n')
            elif mes.find(b'a1 search all\r\n') != -1 and login and selected:
                conn.sendall(b'* SEARCH 1 2\r\n')
            elif mes.find(b'a1 expunge\r\n') != -1 and login and selected:
                conn.sendall(b'* 1 EXPUNGE\r\n')
                conn.sendall(b'A1 OK Expunge completed (0.005 + 0.000 + 0.004 secs).\r\n')
            else:
                conn.sendall(b'A1 BAD Error in IMAP command received by server.\r\n')
        except socket.timeout:
            break
        except ConnectionResetError:
            conn.sendall(b'-ERR The command sent is invalid or unimplemented.\r\n')
        except IndexError:
            conn.sendall(b'-ERR The command sent is invalid or unimplemented.\r\n')
    conn.close()
    print("Connection is close!!!", addr)
