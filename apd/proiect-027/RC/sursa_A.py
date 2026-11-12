# Placa A - sursa semnalului si a listei de membri (Tema 027 RC)
from udp import *
from time import *
import math

PORT = 5000
A_S = 10.0      # amplitudinea sinusoidei
T = 4.0         # perioada, in secunde
FS = 2.0        # rata: esantioane pe secunda
N_MAX = 80      # cate esantioane genereaza A (40 s)

udp = UDPSocket()
membri = []         # IP-urile membrilor grupului
n = 0               # indicele urmatorului esantion
trimiteri = []      # cate datagrame s-au trimis pentru fiecare esantion


def onUDPReceive(ip, port, data):
    # cererile se trateaza aici, generarea din main() nu se opreste
    if data == "JOIN":
        if ip not in membri:
            membri.append(ip)
            print("JOIN de la " + ip + " -> indicele urmatorului esantion: " + str(n) + ", membri: " + str(membri))
        udp.send(ip, PORT, "ACK;JOIN;" + str(n))
    elif data == "LEAVE":
        if ip in membri:
            membri.remove(ip)
            print("LEAVE de la " + ip + " -> indicele urmatorului esantion: " + str(n) + ", membri: " + str(membri))
        udp.send(ip, PORT, "ACK;LEAVE;" + str(n))


def main():
    global n
    udp.onReceive(onUDPReceive)
    udp.begin(PORT)
    print("A porneste: A_s = " + str(A_S) + ", T = " + str(T) + " s, fs = " + str(FS) + " esantioane/s")
    start = uptime()
    while n < N_MAX:
        x = A_S * math.sin(2 * math.pi * n / (T * FS))
        mesaj = "DATA;" + str(n) + ";" + str(round(x, 3))
        destinatari = list(membri)
        for ip in destinatari:
            udp.send(ip, PORT, mesaj)          # cate o datagrama unicast pentru fiecare membru
        trimiteri.append(len(destinatari))
        print("n = " + str(n) + "  x = " + str(round(x, 3)) + "  trimiteri: " + str(len(destinatari)))
        n = n + 1
        asteptare = start + n / FS - uptime()  # urmatorul esantion la start + n/fs
        if asteptare > 0:
            sleep(asteptare)

    for ip in membri:
        udp.send(ip, PORT, "END;" + str(n))
    print("Gata, " + str(n) + " esantioane. Numarul de trimiteri per esantion:")
    for k in range(0, 6):
        cate = trimiteri.count(k)
        if cate > 0:
            print("  " + str(k) + " trimiteri: " + str(cate) + " esantioane")
    print("Total datagrame DATA: " + str(sum(trimiteri)))
    while True:
        sleep(1)


if __name__ == "__main__":
    main()
