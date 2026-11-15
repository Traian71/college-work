# Verificarea calculului de mână de la Subiectul II
import numpy as np, math
f0 = np.array([[100,100,100],[100,200,100],[100,100,100]], dtype=float)
f  = np.array([[112,100, 94],[100,200,100],[106,100, 88]], dtype=float)
M, N = f0.shape
e = f - f0
print('suma f0^2 =', np.sum(f0**2), ' suma e^2 =', np.sum(e**2), ' suma |e| =', np.sum(np.abs(e)))
print('MSE =', np.sum(e**2)/(M*N))
print('MAE =', np.sum(np.abs(e))/(M*N))
print('SNR = %.2f dB' % (10*math.log10(np.sum(f0**2)/np.sum(e**2))))
print('PSNR = %.2f dB' % (10*math.log10(M*N*np.max(f0)**2/np.sum(e**2))))
