import numpy as np, warnings, sys
warnings.filterwarnings('ignore')
sys.path.insert(0, sys.argv[1]); from form_lib import lpc_formants
from scipy.io import wavfile
fs, x = wavfile.read('iom/lab3-bonus/semnale/cuvinte.wav'); x = x / max(abs(x))
zone = {'vin':(0.70,0.83),'merg':(2.40,2.58),'măr':(3.86,4.05),'casă':(5.43,5.56),'mâine':(6.74,6.90),'bun':(8.13,8.28),'nor':(9.47,9.66)}
for c,(t0,t1) in zone.items():
    print('==', c)
    for i in range(int(t0*fs), int(t1*fs), 160):
        print(f'  {i:6d} {i/fs:.2f}s', lpc_formants(x[i:i+160], p=10)[:3])
