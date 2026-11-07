# Spectrograma cuvantului "casă" din inregistrarea mea (lab 3 bonus), cu F1/F2 marcati. Ruleaza din radacina repo.
import numpy as np, warnings
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
fs, x = wavfile.read('iom/lab3-bonus/semnale/cuvinte.wav'); x = x / max(abs(x))
a, b = 42400, 45600
f, t, s = signal.spectrogram(x[a:b], fs, signal.windows.hamming(160), noverlap=140)
fig, ax = plt.subplots(figsize=(7.2, 3.0), dpi=200)
ax.pcolormesh(t, f, 10*np.log10(s + 1e-10), shading='auto', cmap='magma', vmin=-95, vmax=-30)
for fq, lab in ((790, 'F1 ≈ 790 Hz'), (1290, 'F2 ≈ 1290 Hz')):
    ax.annotate(lab, xy=(0.205, fq), xytext=(0.29, fq + 500), color='white', fontsize=9,
                arrowprops=dict(arrowstyle='->', color='white', lw=1))
ax.set_ylim(0, 4000); ax.set_xlabel('Timp [s]'); ax.set_ylabel('Frecvență [Hz]')
ax.set_title('Cuvântul „casă” (înregistrarea mea, 8 kHz): vocala „a”', fontsize=10)
plt.tight_layout(); plt.savefig('arhiva/iom/tema-curs/sursa/fig_casa.png')
print('ok')
