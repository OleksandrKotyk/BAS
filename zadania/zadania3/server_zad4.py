from socket import *
import operator

s = socket(AF_INET, SOCK_DGRAM)
s.bind(("127.0.0.1", 12645))

while True:
    n1, c1 = s.recvfrom(1024)
    opr, c2 = s.recvfrom(1024)
    n2, c3 = s.recvfrom(1024)
    if c1 == c2 == c3:
        ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
        try:
            print(ops[opr.decode("utf-8")](float(n1), float(n2)))
        except:
            print()
            s.sendto(b"Data not correct!!!", c1)
        else:
            s.sendto(str(ops[opr.decode("utf-8")](float(n1), float(n2))).encode("utf-8"), c1)
