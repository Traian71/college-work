#%% 1
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

cale = 'semnale/casa1.wav'
fs,data = wavfile.read(cale)
data = data / max(abs(data))

plt.figure('semnal')
plt.plot(data)
plt.show()

N = int(0.02 * fs)
start_a = 9600
cadru_a = data[start_a:start_a + N]

#%% 2
from scipy import fft
#spectrul de amplitudini
n = 256
sp_a = fft.fft(cadru_a, n = n)
frecv = fft.fftfreq(len(sp_a),1/fs)

plt.figure()
plt.subplot(1,2,1)
plt.plot(range(len(cadru_a)),cadru_a)

plt.subplot(1,2,2)
plt.plot(frecv[:n//2], np.abs(sp_a[:n//2]))
plt.show()

#%% 3
from scipy import signal
# spectrograma
w = signal.windows.hamming(160)
f,t,sxx = signal.spectrogram(data[9300:10200],fs,w)

plt.figure()
plt.pcolormesh(t,f,sxx)
plt.ylabel('Frecventa [Hz]')
plt.xlabel('Timp [s]')
plt.title('Spectrograma')
plt.show()

print(len(t))
