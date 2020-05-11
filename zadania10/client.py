from socket import AF_INET, SOCK_STREAM, socket
from zadania10.functions import get_command

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(("localhost", 125))
socket.settimeout(10)
print(socket.recv(1024))

socket.sendall(b"list_images   \r\n")
list_files = socket.recv(1024).replace(b"List: ", b"")

splt_list_files = list_files.split(b"$")
for i, j in zip(splt_list_files, range(len(splt_list_files))):
    print(str(j + 1) + ":", i.decode("utf-8"))

file_name = b""
while True:
    try:
        numFile = input("Choose file: ")
        if int(numFile) < 1:
            continue
        file_name = splt_list_files[int(numFile) - 1]
    except (IndexError, ValueError):
        continue
    break

socket.sendall(b"get_image: " + file_name + b"   \r\n")
f_command = get_command(socket)

if f_command == b"Not properly file_path!!!\r\n":
    print(f_command)
    exit()

file_size = int(f_command.replace(b"\r\n", b"").decode("utf-8").replace("Size: ", ""))
file_name = get_command(socket).replace(b"\r\n", b"").decode("utf-8").replace("Name: ", "")
print("File_name:", file_name)
print("File_size:", file_size)
image_data = socket.recv(file_size)

f = open(file_name, "wb")
if f.write(image_data) == file_size:
    print("File is added.", end="\n\n")


socket.sendall(b"no_command:\r\n")
print("In case of trouble:")
print(get_command(socket))
