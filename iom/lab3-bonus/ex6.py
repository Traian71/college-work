#%% 6
from scipy.io import wavfile
from scipy import fft, signal
import matplotlib.pyplot as plt
import numpy as np

cale = 'semnale/cuvinte.wav'
fs,data = wavfile.read(cale)
data = data / max(abs(data))

plt.figure('semnal')
plt.plot(data)
plt.show()

cuvinte = ['vin', 'merg', 'mar', 'casa', 'maine', 'bun', 'nor']
limite = [(4000, 7200), (17600, 21200), (29600, 33600), (42400, 45600),
          (53200, 56800), (64000, 67200), (74800, 78400)]
start_vocala = [5920, 20480, 32160, 43920, 54720, 65200, 76560]

N = int(0.02 * fs)
n = 256
w = signal.windows.hamming(160)

for i in range(len(cuvinte)):
    a, b = limite[i]
    f,t,sxx = signal.spectrogram(data[a:b],fs,w)

    cadru = data[start_vocala[i]:start_vocala[i] + N]
    sp = fft.fft(cadru, n = n)
    frecv = fft.fftfreq(len(sp),1/fs)

    plt.figure(cuvinte[i])
    plt.subplot(2,1,1)
    plt.pcolormesh(t,f,sxx)
    plt.ylabel('Frecventa [Hz]')
    plt.xlabel('Timp [s]')
    plt.title('Spectrograma ' + cuvinte[i])

    plt.subplot(2,1,2)
    plt.plot(frecv[:n//2], np.abs(sp[:n//2]))
    plt.xlabel('Frecventa [Hz]')
    plt.title('Spectrul vocalei')
    plt.tight_layout()
    plt.show()
