import cv2
import numpy as np
from matplotlib import pyplot as plt


image = cv2.imread("flower.ppm")
#

def viewImage2(image, transformGray=False, title="Imagem"):
  #h, w, c = image.shape
  try:
    if image.shape[2] > 1 and transformGray:
      image_gray = (cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
      plt.imshow(image_gray, cmap='gray')
    elif image.shape[2] > 1:
      # imagem é colorida
      plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
  except Exception:
      # imagem está em escala de cinza
      plt.imshow(image, cmap='gray')
  finally:
    plt.title(title)
    plt.show()
  
def toGray(image):
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
viewImage2(image, transformGray=True, title="Imagem Monocromática")

def binarizar(image):
  #Binarização da imagem
  #recebe uma imagem COLORIDA 
  img_gray = toGray(image)
  img_bin = np.zeros(shape=(img_gray.shape))
  
  #passa a dimensão y (sao invertidos), mas aqui usa-se o x por convencao
  for x in range(img_bin.shape[0]): 
    for y in range(img_bin.shape[1]):
      #print(img_gray[x][y])
      if img_gray[x][y] <= 128:
        img_bin[x][y] = 0 #ausência de cor é preto (baixa cor)
      else:
        img_bin[x][y] = 1 #muita cor, branco
  return img_bin

viewImage2(binarizar(image), title="Imagem Binarizada")

def subamostragemRGB(image,amostra=2):
  image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #a imagem vem em formato BGR
  new_shape = (int((image.shape[0] + 0.5)/amostra), int((image.shape[1] + 0.5)/amostra), image.shape[2]) #divide a imagem em 1/4
  img_sub = np.zeros(new_shape, dtype=int)
  for x in range(new_shape[0]):
    for y in range(new_shape[1]):
      for z in range(new_shape[2]):
        img_sub[x][y][z] = image[(x*amostra)][(y*amostra)][z]
  return img_sub

viewImage2(image, title="Imagem")  
viewImage2(subamostragemRGB(image, 16), title="Imagem subamostradaRGB")

def subamostragemGray(image, amostra=2):
  img_gray = toGray(image)
  new_shape = (int((img_gray.shape[0] + 0.5)/amostra), int((img_gray.shape[1] + 0.5)/amostra)) #divide a imagem em 1/4
  #print("new shape: ", new_shape)
  img_sub = np.zeros(new_shape)
  #print(img_bin.shape)
  for x in range(new_shape[0]):
    for y in range(new_shape[1]):
      img_sub[x][y] =  int(img_gray[(x*amostra)][(y*amostra)])
  return img_sub

viewImage2(subamostragemGray(image, 16), title="Imagem subamostradaGray")
  


