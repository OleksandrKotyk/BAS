from socket import *

s = socket(AF_INET, SOCK_DGRAM)

print("Postać: liczba operator liczba")
print("Miedzy liczbami a operatorem musi tylko jedna wystąpić spacja!!")

s.settimeout(1)
for j in range(4):
    m = input("Your example: ")
    arr = m.split(" ")
    for i in arr:
        s.sendto(i.encode("utf-8"), ("127.0.0.1", 12645))
    m = s.recvfrom(1024)
    print("Your result: ", m[0].decode("utf-8"))

