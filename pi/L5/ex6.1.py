import numpy as np
import matplotlib as mpl
import math
from matplotlib import pyplot as plt
from skimage import io, color
from scipy import signal


def add_gaussian_noise(img, disp):
    # parametrii : imaginea originala, dispersia zgomotului
    h,w = img.shape
    noise = np.random.normal(0,disp,(h,w))
    img_noise = img + noise
    # intoarce imaginea cu zgomot
    return img_noise

def mse(img, img_modif, capat):
    h,w = img.shape
    delta = img[capat:h-capat,capat:w-capat] - img_modif[capat:h-capat,capat:w-capat]
    delta = delta ** 2
    return np.sum(delta) / ((h-capat*2)*(w-capat*2))

def psnr(img, img_modif, capat):
    mseval = mse(img, img_modif, capat)
    return 20 * math.log10(255) - 10 * math.log10(mseval)


def adaptiv_orientat(vec, size):
    # calculeaza media pe cele 4 directii
    # intoace valoarea cea mai apropiata de valoarea centrala
    # parametrii: vecinatate, dimensiune

    center = size // 2
    # medie orizontala ( 0 grade )
    med0 = np.mean(vec[center, :])
    # medie verticala ( 90 grade )
    med90 = np.mean(vec[:, center])
    # medie diagonala 45 grade
    med45 = 0
    for i in range(size):
        med45 = med45 + vec[size-1-i, i]
    med45 = med45 / size
    # medie diagonala 135 grade
    med135 = 0
    for i in range(size):
        med135 = med135 + vec[i, i]
    med135 = med135 / size
    # calculam diferentele
    # functia pentru modul ( valoare absoluta) este abs()
    delta0 = abs(vec[center, center] - med0)
    delta90 = abs(vec[center, center] - med90)
    delta45 = abs(vec[center, center] - med45)
    delta135 = abs(vec[center, center] - med135)

    # comparam diferentele si intoarcem media corespunzatoare
    # mediei minime
    delta_min = min(delta0, delta90, delta45, delta135)
    if delta_min == delta0:
        return med0
    elif delta_min == delta90:
        return med90
    elif delta_min == delta45:
        return med45
    else:
        return med135


def apply_filter(img, size):
    h, w = img.shape
    capat = size // 2
    # pregatire imagine noua cu zero
    new_img = np.zeros([h,w])
    # parcurgerea imaginii ( atentie la capete )
    for i in range(capat, h-capat):
        for j in range(capat, w-capat):
            # extrage vecinatate
            vec = img[i-capat:i+capat+1, j-capat:j+capat+1]
            # populeaza imaginea noua cu rezultatul filtrarii
            new_img[i,j] = adaptiv_orientat(vec, size)

    # intoarce noul rezultat
    return new_img

# incarca lena.png
img = io.imread('lena.png')
# conversie nivele de gri si gama 0-255, uint 8
img = color.rgb2gray(img)
img = (img * 255).astype(np.uint8)
# afisare imagine originala
plt.figure(), plt.imshow(img, cmap='gray'), plt.title('Imagine originala')

# aplica zgomot
img_noise = add_gaussian_noise(img, 20)
# afiseaza imaginea cu zgomot
plt.figure(), plt.imshow(img_noise, cmap='gray'), plt.title('Imagine cu zgomot')
# afiseaza MSE imagine cu zgomot
print('MSE imagine cu zgomot: {}'.format(mse(img,img_noise,0)))

# setare dimensiune filtru
filter_size = 5
capat = filter_size // 2

# aplicare filtrare mediere
mask = np.ones([filter_size, filter_size]) / (filter_size ** 2)
img_mediere = signal.convolve2d(img_noise, mask, mode='same')
# afiseaza imaginea filtrata prin filtru de mediere
plt.figure(), plt.imshow(img_mediere, cmap='gray'), plt.title('Filtru de mediere')
# afiseaza MSE imagine cu zgomot filtrata prin filtru de mediere
print('MSE imagine filtrata liniar: {}'.format(mse(img,img_mediere,capat)))

# aplicare filtrare adaptiva
img_filt = apply_filter(img_noise, filter_size)
# afiseaza imaginea filtrata prin filtru adaptiv
plt.figure(), plt.imshow(img_filt, cmap='gray'), plt.title('Filtru adaptiv directional')
# afiseaza MSE imagine cu zgomot filtrata prin filtru de mediere
print('MSE imagine filtrata adaptiv: {}'.format(mse(img,img_filt,capat)))

plt.show()
