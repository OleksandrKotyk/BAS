from socket import AF_INET, SOCK_STREAM, socket
from zadania10.functions import *

s = socket(AF_INET, SOCK_STREAM)
s.bind(("localhost", 125))
s.listen(1)

print("Server is on !!!")

run_com = {b"get_image": get_image, b"list_images": list_images}

while True:
    try:
        conn, addr = s.accept()
        conn.sendall(b"You are connected!!!")
        print("Connected to:", addr[0], addr[1])
        while True:
            try:
                command = get_command(conn).replace(b" ", b"").replace(b"\r\n", b"")
                print("Command:", command, "++")
                splt_com = command.split(b":")
                command = splt_com[0].lower()
                run_com[command](conn, splt_com[1:])
            except timeout as e:
                print("Error:", e)
                break
            except KeyError:
                print("Command not found!!!")
                conn.sendall(b"ERROR\r\n")

        conn.close()
    except ConnectionResetError as e:
        print(e)
    print("-------------------------------")
