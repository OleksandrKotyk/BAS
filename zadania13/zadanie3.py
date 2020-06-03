import json
import socket
from threading import Thread, Lock

from zadania13.materials.functions import reach_headers, recv_body, connect, input_user

socket_weather = socket.socket()
lock = Lock()


def get_weather():
    global socket_weather
    try:
        socket_weather.sendall(
            b"GET /data/2.5/weather?appid=d4af3e33095b8c43f1a6815954face64&id=765876 HTTP/1.1\r\n"
            b"HOST: " + socket.gethostbyname("api.openweathermap.org").encode() + b"\r\n\r\n")
        reach_headers(socket_weather, print_headers=False)
        body = recv_body(socket_weather, 4096)
        body_dict = json.loads(body)["main"]
    except (socket.error, OSError):
        socket_weather = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_weather.settimeout(0.5)
        socket_weather.connect((socket.gethostbyname("api.openweathermap.org"), 80))
        socket_weather.sendall(
            b"GET /data/2.5/weather?appid=d4af3e33095b8c43f1a6815954face64&id=765876 HTTP/1.1\r\n"
            b"HOST: " + socket.gethostbyname("api.openweathermap.org").encode() + b"\r\n\r\n")
        reach_headers(socket_weather, print_headers=False)
        body = recv_body(socket_weather, 4096)
        body_dict = json.loads(body)["main"]
    ret = ""
    for i in body_dict:
        ret += i + ": " + str(body_dict[i]) + ", "
    ret = ret[:-2]
    return ret


def irc_start(conf, *msg_list):
    def ssl_send(cmd):
        with lock:
            ssl_sock.write(cmd.encode("utf-8") + b'\r\n')

    def if_quit():
        while True:
            inp = input_user("", False)
            if inp == "QUIT":
                with lock:
                    ssl_sock.write("QUIT".encode("utf-8") + b'\r\n')
                    break
            elif inp.startswith("SEND:"):
                with lock:
                    message = inp[inp.find("SEND: ") + 6:]
                    ssl_sock.write('PRIVMSG #{} :{}'.format(conf['channel'], str(message)).encode("utf-8") + b'\r\n')
            else:
                print("error command")
            # sock.close()

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((irc_config['host'], int(irc_config['port'])))
    ssl_sock = connect(tcp_sock, irc_config['host'], "certs/zadania3.pem")
    if ssl_sock.getpeercert()["issuer"][2][0][1] != "Let's Encrypt Authority X3":
        raise Exception("Issuer error")

    ssl_send('USER {0} localhost localhost {0}'.format(conf['nick']))
    ssl_send('NICK {}'.format(conf['nick']))
    ssl_send('JOIN #{}'.format(conf['channel']))
    for msg in msg_list:
        ssl_send('PRIVMSG #{} :{}'.format(conf['channel'], str(msg)))

    data = b""
    while data.find(b":End of /NAMES list.") == -1:
        data += ssl_sock.read()
    if input_user("Print data y = yes, something else = no:", False) == "y":
        print(data.decode())
    print("Start Listening")
    thread_q = Thread(target=if_quit, args=[])
    thread_q.start()
    while True:
        data = ssl_sock.read()
        print(data.decode(), end="")
        if data == b'':
            print("Stop bot")
            break
        for msg in data.split(b"\r\n"):
            if msg.startswith(b"PING "):
                ssl_send('PONG {} {}'.format(conf['channel'], msg[5:].decode("utf-8")))
                print('PONG {} {}'.format(conf['channel'], msg[5:].decode("utf-8")), "::::::::: SEnDED")
            if msg.find(b"PRIVMSG") != -1:
                mes = msg[msg.find(b":", 1) + 1:].decode()
                if mes == "pogoda lublin":
                    ssl_send('PRIVMSG #{} :{}'.format(conf['channel'], get_weather()))


irc_config = {
    'host': "chat.freenode.net",
    'port': '7000',
    'nick': 'okotyk_weather_bot',
    'channel': 'tell_mew_weather_please'
}

# SEND: something  - jeżeli wpisać w konsoli bot a to można wysyłać wiadomość
# QUIT - stop bot, wysyła 'QUIT' do serwera
# jeżeli użytkownik napisze 'pogoda lublin' to bot wyśle informacje o pogodzie
irc_start(irc_config, "Hello, im a weather bot, 'pogoda lublin' = send weather information")
