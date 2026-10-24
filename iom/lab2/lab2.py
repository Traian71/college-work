#%% 1) Citirea si interpretarea unui semnal vocal
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

cale = 'semnale/casa1.wav'
fs,data = wavfile.read(cale)
data = data / max(abs(data))

plt.figure('semnal')
plt.plot(data)
plt.show()

a = data[9600:9760]

#%% 2) Extragerea cate unui cadru de 20 ms din "a" si "s"
N = int(0.02 * fs)      # 20 ms la fs = 8000 Hz -> 160 esantioane

start_a = 9600          # mijlocul lui "a" (aprox. 1.14 - 1.30 s)
stop_a = start_a + N    # 9760
start_s = 10960         # mijlocul lui "s" (aprox. 1.33 - 1.43 s)
stop_s = start_s + N    # 11120

cadru_a = data[start_a:stop_a]
cadru_s = data[start_s:stop_s]

plt.figure('cadru a')
plt.plot(cadru_a)
plt.title('Cadrul "a" [9600:9760]')
plt.show()

plt.figure('cadru s')
plt.plot(cadru_s)
plt.title('Cadrul "s" [10960:11120]')
plt.show()

#%% 3) Parametrii de timp scurt
def energie(x):
    return np.sum(x**2)

def treceri_zero(x):
    # fereastra dreptunghiulara w(n) = 1/(2N)
    return np.sum(np.abs(np.diff(np.sign(x)))) / (2 * len(x))

def autocorelatie(x):
    N = len(x)
    R = np.zeros(N)
    for k in range(N):
        R[k] = np.sum(x[0:N-k] * x[k:N])
    return R

Ea = energie(cadru_a)
Za = treceri_zero(cadru_a)
Ra = autocorelatie(cadru_a)

Es = energie(cadru_s)
Zs = treceri_zero(cadru_s)
Rs = autocorelatie(cadru_s)

# maximul autocorelatiei normate pentru k intre 16 si 133 (F0 intre 60 si 500 Hz)
ka = 16 + np.argmax(Ra[16:134])
ks = 16 + np.argmax(Rs[16:134])

print('Ea =', round(Ea, 3), '; Za =', round(Za, 3), '; Ra =', round(Ra[ka] / Ra[0], 2), 'la k =', ka)
print('Es =', round(Es, 3), '; Zs =', round(Zs, 3), '; Rs =', round(Rs[ks] / Rs[0], 2), 'la k =', ks)
# Ea = 6.69 ; Za = 0.244 ; Ra = 0.7 la k = 29
# Es = 0.018 ; Zs = 0.425 ; Rs = 0.14 la k = 27
# "a" (sonor): energie mare, putine treceri prin zero, autocorelatie periodica
# "s" (nesonor): energie mica, multe treceri prin zero, autocorelatie fara maxime clare

plt.figure('autocorelatie')
plt.plot(Ra / Ra[0], label='a')
plt.plot(Rs / Rs[0], label='s')
plt.legend()
plt.show()
