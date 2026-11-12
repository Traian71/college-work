# Placile B, C, D, E - membrii grupului (Tema 027 RC)
# Se schimba doar JOIN_DUPA si LEAVE_DUPA:
#   B, D: JOIN_DUPA = 0,  LEAVE_DUPA = -1
#   C:    JOIN_DUPA = 0,  LEAVE_DUPA = 45   (se retrage in timpul rularii)
#   E:    JOIN_DUPA = 15, LEAVE_DUPA = -1   (se inscrie dupa inceperea fluxului)
from udp import *
from time import *

IP_A = "192.168.1.1"
PORT = 5000
JOIN_DUPA = 0       # secunde de la pornirea programului pana la JOIN
LEAVE_DUPA = -1     # secunde pana la LEAVE (-1 = nu se retrage)

udp = UDPSocket()
stare = "IN_AFARA"  # IN_AFARA -> IN_GRUP -> RETRAS
primul = -1
ultimul = -1
primite = 0
dupa_leave = 0      # esantioane sosite dupa trimiterea LEAVE
leave_trimis = False


def rezumat():
    print("Primul indice primit: " + str(primul) + ", ultimul: " + str(ultimul) + ", primite: " + str(primite))


def onUDPReceive(ip, port, data):
    global stare, primul, ultimul, primite, dupa_leave
    parti = data.split(";")
    if parti[0] == "DATA":
        idx = int(parti[1])
        if primul < 0:
            primul = idx
            print("Primul esantion primit: n = " + str(idx))
        ultimul = idx
        primite = primite + 1
        if leave_trimis:
            dupa_leave = dupa_leave + 1
        print("n = " + parti[1] + "  x = " + parti[2])
    elif parti[0] == "ACK" and parti[1] == "JOIN" and stare == "IN_AFARA":
        stare = "IN_GRUP"
        print("A a confirmat JOIN, indicele urmator la A: " + parti[2])
    elif parti[0] == "ACK" and parti[1] == "LEAVE" and stare == "IN_GRUP":
        stare = "RETRAS"
        print("A a confirmat LEAVE, indicele urmator la A: " + parti[2])
        print("Esantioane primite dupa trimiterea LEAVE: " + str(dupa_leave))
        rezumat()
    elif parti[0] == "END":
        print("Fluxul s-a terminat la A (" + parti[1] + " esantioane)")
        rezumat()


start = 0


def main():
    global start, leave_trimis
    udp.onReceive(onUDPReceive)
    udp.begin(PORT)
    start = uptime()
    ultima_cerere = -10
    while True:
        t = uptime() - start
        # cererile se repeta la 1 s pana vine confirmarea
        if stare == "IN_AFARA" and t >= JOIN_DUPA and t - ultima_cerere >= 1:
            udp.send(IP_A, PORT, "JOIN")
            ultima_cerere = t
            print("Trimit JOIN la A")
        if stare == "IN_GRUP" and LEAVE_DUPA >= 0 and t >= LEAVE_DUPA and t - ultima_cerere >= 1:
            udp.send(IP_A, PORT, "LEAVE")
            leave_trimis = True
            ultima_cerere = t
            print("Trimit LEAVE la A")
        sleep(0.2)


if __name__ == "__main__":
    main()
