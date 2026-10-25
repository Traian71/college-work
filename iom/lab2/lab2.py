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

a = data[9600:9760]

#%% 2
N = int(0.02 * fs)

start_a = 9600
stop_a = start_a + N
a = data[start_a:stop_a]

start_s = 10960
stop_s = start_s + N
s = data[start_s:stop_s]

plt.figure('a')
plt.plot(a)
plt.show()

plt.figure('s')
plt.plot(s)
plt.show()

#%% 3
def energie(x):
    E = 0
    for m in range(len(x)):
        E = E + x[m]**2
    return E

def treceri_zero(x):
    Z = 0
    for m in range(1, len(x)):
        Z = Z + abs(np.sign(x[m]) - np.sign(x[m-1]))
    return Z / (2 * len(x))

def autocorelatie(x):
    N = len(x)
    R = np.zeros(N)
    for k in range(N):
        for m in range(N - k):
            R[k] = R[k] + x[m] * x[m+k]
    return R

Ea = energie(a)
Za = treceri_zero(a)
Ra = autocorelatie(a)

Es = energie(s)
Zs = treceri_zero(s)
Rs = autocorelatie(s)

print('Ea =', Ea, 'Za =', Za)
print('Es =', Es, 'Zs =', Zs)

plt.figure('Ra')
plt.plot(Ra)
plt.show()

plt.figure('Rs')
plt.plot(Rs)
plt.show()

#%% 5
cale = 'semnale/semnal_propriu.wav'
fs,data = wavfile.read(cale)
data = data / max(abs(data))

plt.figure('semnal propriu')
plt.plot(data)
plt.show()

a = data[7600:7600 + N]
s = data[8840:8840 + N]

Ea = energie(a)
Za = treceri_zero(a)
Ra = autocorelatie(a)

Es = energie(s)
Zs = treceri_zero(s)
Rs = autocorelatie(s)

print('Ea =', Ea, 'Za =', Za)
print('Es =', Es, 'Zs =', Zs)

plt.figure('Ra propriu')
plt.plot(Ra)
plt.show()

plt.figure('Rs propriu')
plt.plot(Rs)
plt.show()
