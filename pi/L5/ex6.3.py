import numpy as np
import matplotlib as mpl
import math
from matplotlib import pyplot as plt
from skimage import io, color
from scipy import signal


def add_gaussian_noise(img, disp):
    # adauga zgomot gausian asupra imaginii
    # parametrii: imaginea originala, dispersia zgomotului
    h,w = img.shape
    noise = np.random.normal(0,disp,(h,w))
    img_noise = img + noise
    return img_noise

def mse(img, img_modif, capat):
    h,w = img.shape
    delta = img[capat:h-capat,capat:w-capat] - img_modif[capat:h-capat,capat:w-capat]
    delta = delta ** 2
    return np.sum(delta) / ((h-capat*2)*(w-capat*2))

def psnr(img, img_modif, capat):
    mseval = mse(img, img_modif, capat)
    return 20 * math.log10(255) - 10 * math.log10(mseval)


def llmmse(vec, size, disp):
    # calculeaza media pe cele 4 directii
    # intoace valoarea cea mai apropiata de valoarea centrala
    # parametrii: vecinatate, dimensiune, dispersia zgomotului

    center = size // 2
    # medie aritmetica
    med = np.sum(vec) / (size ** 2)
    # calcul varianta vecinatate
    var = np.var(vec)

    # calcul alfa
    # atentie, varianta este disperisa la patrat
    alpha = 1 - disp ** 2 / var
    if alpha < 0:
        alpha = 0
    # calcul valoare finala
    return alpha * vec[center, center] + (1 - alpha) * med

def apply_filter(img, size, disp):
    # aplica filtrul llmmse
    # parametrii: imaginea, dimensiunea ferestrei, dispersia zgomotului
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
            new_img[i,j] = llmmse(vec, vec.shape[0], disp)

    # intoarce noul rezultat
    return new_img

# incarca lena.png
img = io.imread('lena.png')
# conversie nivele de gri si gama 0-255, uint 8
img = np.uint8(color.rgb2gray(img)*255)
# afisare imagine originala
plt.figure(), plt.imshow(img, cmap='gray')


# aplica zgomot
img_noise = add_gaussian_noise(img, 20)
# afiseaza imaginea cu zgomot
plt.figure(), plt.imshow(img_noise, cmap='gray')
# afiseaza MSE imagine cu zgomot
print('MSE imagine cu zgomot: {}'.format(mse(img, img_noise, 0)))

# setare dimensiune filtru
filter_size = 7
capat = filter_size // 2

# aplicare filtrare mediere
mask = np.ones([filter_size, filter_size]) / (filter_size ** 2)
img_mediere = signal.convolve2d(img_noise, mask, mode='same')
# afiseaza imaginea filtrata prin filtru de mediere
plt.figure(), plt.imshow(img_mediere, cmap='gray')
# afiseaza MSE imagine cu zgomot filtrata prin filtru de mediere
print('MSE imagine filtrata liniar: {}'.format(mse(img, img_mediere, capat)))

# aplicare filtrare adaptiva
img_filt = apply_filter(img_noise, filter_size, 20)
# afiseaza imaginea filtrata prin filtru adaptiv
plt.figure(), plt.imshow(img_filt, cmap='gray')
# afiseaza MSE imagine cu zgomot filtrata prin filtru de mediere
print('MSE imagine filtrata adaptiv: {}'.format(mse(img, img_filt, capat)))

plt.show()
