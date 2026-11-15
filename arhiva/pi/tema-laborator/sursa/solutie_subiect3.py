# Soluția de referință pentru Subiectul III (folosită la barem)
import numpy as np
import math
import matplotlib.pyplot as plt
from skimage import io, color
from scipy import signal

def mse(f0, f):
    h, w = f0.shape
    return np.sum((f - f0) ** 2) / (h * w)

def snr(f0, f):
    return 10 * math.log10(np.sum(f0 ** 2) / np.sum((f - f0) ** 2))

def psnr(f0, f):
    h, w = f0.shape
    return 10 * math.log10(h * w * np.max(f0) ** 2 / np.sum((f - f0) ** 2))

# imaginea de referință f0, nivele de gri în [0,255]
img = io.imread('lena.png')
img = color.rgb2gray(img) * 255
h, w = img.shape

# imaginea degradată: zgomot gaussian de medie 0 și sigma 10
np.random.seed(0)
N = np.random.normal(0, 10, (h, w))
img_noise = img + N

# filtrare de mediere aritmetică 3x3
mask = np.ones([3, 3]) / 9
img_filt = signal.convolve2d(img_noise, mask, mode='same', boundary='symm')

print('zgomotoasa: MSE = %.2f  SNR = %.2f dB  PSNR = %.2f dB' % (mse(img, img_noise), snr(img, img_noise), psnr(img, img_noise)))
print('filtrata:   MSE = %.2f  SNR = %.2f dB  PSNR = %.2f dB' % (mse(img, img_filt), snr(img, img_filt), psnr(img, img_filt)))

plt.figure(), plt.imshow(img_noise, cmap='gray')
plt.figure(), plt.imshow(img_filt, cmap='gray')
# plt.show()

# --- verificări (nu fac parte din soluția cerută) ---
print('max f0 =', np.max(img))
print('PSNR cu 255 (ca in Lab 4): zg %.2f  filt %.2f' % (10*math.log10(255**2/mse(img,img_noise)), 10*math.log10(255**2/mse(img,img_filt))))
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio
print('skimage MSE:', mean_squared_error(img, img_noise), mean_squared_error(img, img_filt))
print('skimage PSNR (data_range=max f0):', peak_signal_noise_ratio(img, img_noise, data_range=np.max(img)), peak_signal_noise_ratio(img, img_filt, data_range=np.max(img)))
for s in (1, 2, 42):
    np.random.seed(s); Nn = np.random.normal(0, 10, (h, w)); a = img + Nn
    b = signal.convolve2d(a, mask, mode='same', boundary='symm')
    print('seed', s, round(mse(img,a),2), round(snr(img,a),2), round(psnr(img,a),2), '|', round(mse(img,b),2), round(snr(img,b),2), round(psnr(img,b),2))
# fara boundary='symm' (zero padding)
c = signal.convolve2d(img_noise, mask, mode='same')
print('zero padding: MSE %.2f SNR %.2f PSNR %.2f' % (mse(img,c), snr(img,c), psnr(img,c)))
