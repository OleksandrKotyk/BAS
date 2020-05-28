from queue import Queue, Empty
from select import select
from socket import AF_INET, SOCK_STREAM, socket, error

buf_size = 1024

socket = socket(AF_INET, SOCK_STREAM)
socket.setblocking(False)
socket.bind(("localhost", 125))
socket.listen(10)
inputs = [socket]
outputs = []

message_queues = {}

while inputs:
    readable, writable, exceptional = select(inputs, outputs, inputs)
    for s in readable:
        if s is socket:
            conn, addr = s.accept()
            print("Conected:", conn)
            conn.setblocking(False)
            conn.sendall(b"Hello")
            inputs.append(conn)
            message_queues[conn] = Queue()
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
                message_queues[s].put(data)
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
