import matplotlib.pyplot as plt
import numpy as np
from skimage import io,util,color
import math
import time

#aplica media aritmetica pentru o vecinatate
#sunt 2 variante, una clasica si una scurta cu np.sum()
def smooth(window, w_size):
    
    #PARAMETERS : fereastra,dim ferestrei
    #RETURN  :   media aritmetica a pixelilor din fereastra
    suma=0
    suma = np.sum(window)
    return suma/w_size**2
    #Varianta 1
    # se parcurge fereaastra si se calculeaza media aritmetica
    
    #Varianta 2
    # se realizeaza aceeasi operatie folsind np.sum() 
    
def filt_mediere_aritm(img, h, w, w_size, capat):
    
    #PARAMETERS : imaginea,dim imaginii,dim ferestrei, capat
    #RETURN  :   imag filtrata
    
    #initializez imaginea pentru filtrare cu 0
    img_new= np.zeros((h-2*capat, w-2*capat))
    #parcurg imaginea, decupez si aplic functia scrisa anterior pentru fiecare fereastra
    for i in range(capat, h-capat):
        for j in range(capat, w-capat):
            window = img[i-capat:i+capat+1, j-capat:j+capat+1]
            img_new[i-capat, j-capat] = smooth(window, w_size)
    #returnez imag_filtra
    return img_new
    
# Citesc imag color    
img = io.imread('lena.png')
print(img.dtype)

# transform in gray imaginea si schimb gama in   [0,255]
img = np.uint8(color.rgb2gray(img)*255)
#dimensiunea imaginii
h,w=img.shape

# afisez imaginea gray
plt.figure(),plt.imshow(img,cmap='gray')

#adaug zgomot in imagine si afizes imaginea zgomotosa
#zgomot de medie 0 dispersie sigma 
sigma=10
N=np.random.normal(0,sigma,(h, w))

#adun zgomotul in imagine si afisez
img_noise=img+N
plt.figure(),plt.imshow(img_noise,cmap='gray')

#dim ferestrei si numarul de linii si coloane care se pierd pt fiecare tip de fereastra
window_size=3
capat=math.floor(window_size/2)

b=time.time()

#aplic functia de filtrare liniara scrisa mai sus
img_filt=filt_mediere_aritm(img_noise, h, w, window_size, capat)

e=time.time()
print('timp executie: ',e-b)

#afisez imaginea filtrata
plt.figure(), plt.imshow(img_filt, cmap='gray')