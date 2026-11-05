# Completeaza fisa L3 cu raspunsurile si graficele (ruleaza din radacina repo-ului).
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import fft, signal
import docx
from docx.shared import Pt, Cm

SURSA = 'arhiva/iom/lab3/sursa'
FISA_IN = 'arhiva/iom/lab3/materiale/L3_AnalizaInFrecventa.docx'
FISA_OUT = 'iom/lab3/L3_AnalizaInFrecventa.docx'

fs, data = wavfile.read('iom/lab3/semnale/casa1.wav')
data = data / max(abs(data))
cadru_a = data[9600:9760]
n = 256
sp_a = fft.fft(cadru_a, n=n)
frecv = fft.fftfreq(len(sp_a), 1/fs)

plt.figure(figsize=(8, 3))
plt.subplot(1, 2, 1)
plt.plot(range(len(cadru_a)), cadru_a)
plt.title('cadru_a')
plt.subplot(1, 2, 2)
plt.plot(frecv[:n//2], np.abs(sp_a[:n//2]))
plt.title('Spectrul de amplitudine')
plt.xlabel('Frecventa [Hz]')
plt.tight_layout()
plt.savefig(f'{SURSA}/spectru.png', dpi=150)

w = signal.windows.hamming(160)
f, t, sxx = signal.spectrogram(data[9300:10200], fs, w)
plt.figure(figsize=(8, 3))
plt.pcolormesh(t, f, sxx)
plt.ylabel('Frecventa [Hz]')
plt.xlabel('Timp [s]')
plt.title('Spectrograma')
plt.tight_layout()
plt.savefig(f'{SURSA}/spectrograma.png', dpi=150)

d = docx.Document(FISA_IN)
tab = d.tables[2]


def scrie(rand, linii, imagine=None, cod=False):
    c = tab.rows[rand].cells[1]
    p = c.paragraphs[0]
    for i, linie in enumerate(linii):
        if i > 0:
            p = c.add_paragraph(style=c.paragraphs[0].style)
        r = p.add_run(linie)
        if cod:
            r.font.name = 'Consolas'
            r.font.size = Pt(10)
    if imagine:
        c.add_paragraph(style=c.paragraphs[0].style).add_run().add_picture(imagine, width=Cm(14))


scrie(1, [
    "fs,data = wavfile.read('semnale/casa1.wav')",
    "data = data / max(abs(data))",
    "N = int(0.02 * fs)",
    "start_a = 9600",
    "cadru_a = data[start_a:start_a + N]",
], cod=True)
tab.rows[1].cells[1].add_paragraph(
    'Cadru de 20 ms (160 eșantioane), eșantioanele 9600–9760, de pe la jumătatea lui „a”.',
    style=tab.rows[1].cells[1].paragraphs[0].style)

scrie(4, [
    'Codul folosește cadru_a de la ex. 1 și variabila n în apelul FFT: sp_a = fft.fft(cadru_a, n = n) (lab3.py, celula 2).',
    'n este numărul de puncte în care se calculează FFT. Trebuie să fie putere a lui 2 și cel puțin egal cu numărul de '
    'eșantioane din cadru: cadrul are 160 de eșantioane, deci n = 256 (restul se completează cu zerouri).',
    'Spectrul unui semnal real este simetric față de fs/2, a doua jumătate corespunde frecvențelor negative și repetă prima '
    'jumătate, așa că se afișează doar 0–fs/2 (0–4000 Hz). FFT dă numere complexe (amplitudine și fază), iar modulul dă '
    'amplitudinea fiecărei componente de frecvență.',
], imagine=f'{SURSA}/spectru.png')

scrie(7, [
    'f = vectorul de frecvențe (0–4000 Hz, din 50 în 50 Hz); t = momentele de timp (centrele cadrelor) pentru care s-a '
    'calculat spectrul; Sxx = matricea spectrogramei, puterea semnalului pentru fiecare frecvență din f și fiecare moment '
    'din t; w = fereastra Hamming de 160 de eșantioane (20 ms) aplicată pe fiecare cadru.',
    'Secvența 9300–10200 aparține fonemului „a” din prima rostire a cuvântului „casă”.',
    'Spectrograma este calculată pentru 6 cadre (len(t) = 6): 900 de eșantioane, fereastră de 160, suprapunere implicită '
    'de 20, deci pas de 140 → (900 − 160) / 140 + 1 = 6.',
    f'Se observă 2 formanți: F1 ≈ 800 Hz și F2 ≈ 1600 Hz, apropiați de valorile din tabel pentru „a” (850 și 1500 Hz).',
], imagine=f'{SURSA}/spectrograma.png')

scrie(10, [
    'Da. Fiecare coloană din spectrogramă este spectrul de putere al unui cadru de 20 ms (pătratul spectrului de '
    'amplitudine, calculat cu fereastră Hamming). Vârfurile din spectrul de amplitudine (≈ 800 Hz și ≈ 1600 Hz) apar în '
    'spectrogramă ca benzi deschise la aceleași frecvențe. În plus, spectrograma arată cum se schimbă spectrul în timp.',
])

scrie(12, [
    'Codul interfeței: GUI_ex5.py.',
    'Se alege fișierul .wav, eșantionul de start și de stop al cadrului și fereastra spectrogramei (ms); n se alege '
    'automat ca prima putere a lui 2 ≥ lungimea cadrului.',
    'Pentru casa1.wav, cadrul 9300–10200 (n = 1024): formanți la ≈ 800 Hz și ≈ 1600 Hz, ca la ex. 3.',
])

d.save(FISA_OUT)
print('ok')
