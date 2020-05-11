from time import time
from os.path import getsize, basename
from os import listdir
from socket import timeout


def get_command(sock, stop_chars=b"\r\n"):
    ln_stp_ch = len(stop_chars)

    time_out_time = 10
    sock.settimeout(time_out_time)
    start = time()

    cmn = b""
    while True:
        b = sock.recv(1)
        cmn += b

        start = time() if b != b'' else start
        if time() - start > time_out_time:
            raise timeout(time() - start)
        elif len(cmn) >= ln_stp_ch and cmn[-ln_stp_ch:] == stop_chars:
            return cmn


def lst_dir(drc, rem="$"):
    files = listdir(drc)
    for i in range(len(files)):
        files[i] = files[i].replace(rem, "")
    return files


def get_image(sock, params, path="david-anderson-yQOu28ZlkHo-unsplash.jpg", directory="Images"):
    path = params[0] if len(params) > 0 else path
    path = path.decode("utf-8")
    if path not in lst_dir(directory):
        sock.sendall(b"Not properly file path!!!\r\n")
        return

    full_path = directory + "/" + path
    with open(full_path, "rb") as image:
        size = str(getsize(full_path)).encode("utf-8")
        base = basename(full_path).encode("utf-8")
        f = image.read()
        b = bytearray(f)
        sock.sendall(b"Size: " + size + b"\r\n")
        sock.sendall(b"Name: " + base + b"\r\n")
        sock.sendall(b)
        print("Send image data!!!")


def list_images(sock, params, directory="Images"):
    images = lst_dir(directory)

    to_send = "List: " + "$".join(images) + "\r\n"
    sock.sendall(to_send.encode("utf-8"))
