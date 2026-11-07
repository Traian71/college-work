import numpy as np
from scipy import signal
fs = 8000
def lpc_formants(fr, p=10):
    fr = signal.lfilter([1,-0.97],1,fr) * np.hamming(len(fr))
    r = np.correlate(fr, fr, 'full')[len(fr)-1:len(fr)+p]
    a = np.zeros(p+1); a[0]=1; e=r[0]
    for i in range(1,p+1):
        k = -(r[i]+np.dot(a[1:i], r[i-1:0:-1]))/e
        a[1:i+1] = a[1:i+1] + k*np.concatenate((a[i-1:0:-1],[1]))
        e *= 1-k*k
    rts = [z for z in np.roots(a) if np.imag(z) > 0]
    f = sorted((np.angle(z)*fs/(2*np.pi), -fs/np.pi*np.log(abs(z))) for z in rts)
    return [round(fq) for fq, bw in f if fq > 150 and bw < 500]
