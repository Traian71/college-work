import numpy as np, warnings, sys
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
sys.path.insert(0, sys.argv[1]); from form_lib import lpc_formants
fs, x = wavfile.read('iom/lab3-bonus/semnale/cuvinte.wav'); x = x / max(abs(x))
segs = [(5440,6720),(18560,20640),(30720,32000),(43520,44320),(53920,55840),(64960,66400),(75360,77280)]
cuv = ['vin','merg','măr','casă','mâine','bun','nor']
fig, axs = plt.subplots(7, 1, figsize=(10, 22))
for ax, (a, b), c in zip(axs, segs, cuv):
    a0, b0 = a - 2400, b + 2400
    y = x[a0:b0]
    f, t, s = signal.spectrogram(y, fs, signal.windows.hamming(160), noverlap=120)
    ax.pcolormesh(t + a0/fs, f, 10*np.log10(s + 1e-10), shading='auto', cmap='magma')
    E = np.array([np.sum(x[i:i+160]**2) for i in range(a0, b0-160, 80)])
    for k, i in enumerate(range(a0, b0-160, 80)):
        if E[k] > 0.15*E.max():
            for fq in lpc_formants(x[i:i+160])[:3]:
                ax.plot((i+80)/fs, fq, 'c.', ms=4)
    ax.set_ylim(0, 4000); ax.set_title(f'{c}  (eșantioane {a0}-{b0})'); ax.axvspan(a/fs, b/fs, color='w', alpha=.08)
plt.tight_layout(); plt.savefig(sys.argv[1] + '/tracks.png', dpi=70)
