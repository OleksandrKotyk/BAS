import socket

from zadania13.materials.functions import connect, reach_headers, recv_body, input_user

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostbyname("httpbin.org"), 443))
sock = connect(sock, "httpbin.org", "certs/main.crt", ask=True)
sock.write(b"GET /html HTTP/1.1\r\n"
           b"HOST: 212.182.24.27\r\n"
           b"User-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) "
           b"Version/7.0.3 Safari/7046A194A\r\n\r\n")

sock.settimeout(1)
html_len = int(reach_headers(sock, b"Content-Length:"))
body = recv_body(sock, html_len)

file_name = input_user("file_name: ", False)
file_name += ".html" if file_name.find(".html") == -1 else ""

f = open(file_name, "w")
f.write(body.decode("windows-1251"))
f.close()

sock.close()
