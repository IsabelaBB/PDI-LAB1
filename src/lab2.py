#!/usr/bin/python3

import cv2
import numpy as np
import sys
import os
import matplotlib
import math
from matplotlib import pyplot as plt
# Agg backend runs without a display
matplotlib.use( 'tkagg' )
from skimage.measure import compare_ssim
from utils import options, saveChanges
import lab1

'''
TRABALHO EM GRUPO DE NO MÁXIMO 5 PESSOAS ENVIAR LINK PARA ACESSO A TODOS OS CÓDIGOS, 
ARQUIVO EXECUTÁVEL E EXPLICAÇÕES NECESSÁRIAS (incluindo instruções para instalar compiladores e bibliotecas). 
******************************************************************* 
Implementação em PHYTON, JAVA, C ou C++ de códigos para: 
- Operações de realce (transformações de intensidade), 
sendo, no mínimo: negativo, binarização e equalização de histogramas.
'''


# negativo de imagem
# recebe uma imagem (BGR ou gray), imprime o negativo da imagem
# e retorna uma imagem (original ou negativa)
def negative(image):

  '''
    Input: imagem BGR
    Output: None
  '''

  if len(image.shape) > 2:

    #separa as componentes RGB  
    B, G, R = cv2.split(image)
  
    #inverte cada componente
    B_neg = 255-B
    G_neg = 255-G
    R_neg = 255-R

    #merge das componentes
    im_neg = cv2.merge([B_neg, G_neg, R_neg])
  
    # converte para escala de cinza
    im_neg_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # inverte 
    im_neg_gray = 255 - im_neg_gray

    # exibe as imagens
    lab1.viewImages([im_neg, im_neg_gray], ['Imagem Negativa', 'Imagem negativa Escala de Cinza'])

  else:
    im_neg = 255 - image # inverte
    lab1.viewImage(im_neg, 'imagem negativa') # exibe a imagem
    
  return saveChanges(image, im_neg)
  


# Equalização de histograma
# com os tres canais de cores (resultado estranho)
def equalizeHist(image):

  if len(image.shape) < 3:
    print('Essa opção só é válida para imagens coloridas')
    print('<Pressione ENTER para continuar>')
    input()
    return image

  #Separa as componentes da imagem colorida
  B, G, R = cv2.split(image)

  #Equalizando cada componente separadamente
  B_eq = cv2.equalizeHist(B)
  G_eq = cv2.equalizeHist(G)
  R_eq = cv2.equalizeHist(R)

  #uni as componentes
  image_eq = cv2.merge([B_eq, G_eq,R_eq])

  # plota imagens e histogramas
  f = plt.figure()

  f.add_subplot(2,2,1)
  plt.title('Imagem original')
  plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))

  f.add_subplot(2,2,2)
  plt.title('Imagem equalizada')
  plt.imshow(cv2.cvtColor(image_eq,cv2.COLOR_BGR2RGB))

  f.add_subplot(2,1,2)
  plt.title('Histograma')
  plt.plot(cv2.calcHist([image_eq],[0],None,[256],[0,255]), color='gray')

  plt.show()

  return saveChanges(image, image_eq)



# Equalização de histograma
# recebe uma imagem BGR
def equalizeHist_gray(image):
  original = image

  if len(image.shape) > 2:
    print('Essa opção só é válida para imagens em tons de cinza')
    print('<Pressione ENTER para continuar>')
    input()
    return image

  # probabilidade
  p = np.zeros(256)

  # esse v_min é a intensidade mínima em cada canal de cor
  v_min = [256] # o valor real (da formula) de v_min é vr[v_min[0]], por exemplo
  
  # probabilidade acumulada
  v = np.zeros(256)

  # calcula valores de p e v_min
  h, w = image.shape
  for x in range(w):
    for y in range(h):
      if image[y,x] < v_min:
        v_min = image[y,x]

      p[image[y,x]] += 1
      
  # calcula valores de v
  v[0] = p[0]/(w*h)
  for i in range(255):
    i += 1
    v[i] = v[i-1] + p[i]/(w*h)

  # atualiza os valores da imagem (valores v*)
  for x in range(w):
    for y in range(h):
      image[y,x] = int((v[image[y,x]] - v[v_min]) / (1 - v[v_min])*255 +0.5)

  # plota imagens e histogramas
  f = plt.figure()

  f.add_subplot(2,2,1)
  plt.title('Imagem original')
  plt.imshow(original, cmap='gray')

  f.add_subplot(2,2,2)
  plt.title('Imagem equalizada')
  plt.imshow(image, cmap='gray')

  f.add_subplot(2,1,2)
  plt.title('Histograma')
  plt.plot(cv2.calcHist([image],[0],None,[256],[0,255]), color='gray')

  plt.show()

  # exibe
  #lab1.viewImages([original, image], ['Imagem original', 'Imagem equalizada'])
  #lab1.viewHistograms(image)
  
  return saveChanges(original, image)



def trans_intensidade_gray(image,a=80,b=160,alfa=40,beta=10, charlie=-30):
  original = image
  if len(image.shape) > 2:
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

  for i in range(image.shape[0]):
    for j in range(image.shape[1]):

      if image[i][j] < a:
        image[i][j]  = image[i][j]  + alfa
      elif image[i][j] > a and image[i][j] < b:
        image[i][j]  = image[i][j]  + beta
      else:
        image[i][j]  = image[i][j]  + charlie

  #plt.imshow(image, cmap='gray')
  # plota imagens e histogramas
  f = plt.figure()

  f.add_subplot(2,2,1)
  plt.title('Imagem original')
  plt.imshow(cv2.cvtColor(original,cv2.COLOR_BGR2RGB))

  f.add_subplot(2,2,2)
  plt.title('Imagem transformada')
  plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))

  f.add_subplot(2,2,3)
  plt.title('Histograma da imagem original')
  plt.plot(cv2.calcHist([original],[0],None,[256],[0,255]))

  f.add_subplot(2,2,4)
  plt.title('Histograma da imagem transformada')
  plt.plot(cv2.calcHist([image],[0],None,[256],[0,255]))

  plt.show()

  return saveChanges(original, image)


'''
Essa funcao aplica a formula abaixo à imagem
s = c*e^gamma
s - saída
e - entrada

c e gamma são constantes
'''
def trans_potencia(image):
  original = image
  c = 1
  gamma = 2.5
  
  altura = original.shape[0]
  largura = original.shape[1]
  
  #se a imagem for RGB
  if len(original.shape) > 2 :
    dimensoes = original.shape[2]
    #matriz de saída
    image = np.zeros((altura,largura,dimensoes),dtype=np.float32)
    
    #percorrendo a imagem para aplicacao da formula
    for i in range(altura):
        for j in range(largura):
            for k in range(dimensoes):
              image[i,j,k] = c*math.pow(original[i, j, k], gamma)
            
  #caso, contrário  
  else:
    image = np.zeros((altura,largura,1),dtype=np.float32)
    
    for i in range(altura):
        for j in range(largura):
              image[i,j] = c*math.pow(original[i, j], gamma)
            
  #normalizacao da imagem [0,255]            
  cv2.normalize(image,image,0,255,cv2.NORM_MINMAX)
  image = cv2.convertScaleAbs(image)
  
  # plota imagens e histogramas
  f = plt.figure()

  f.add_subplot(2,2,1)
  plt.title('Imagem original')
  plt.imshow(cv2.cvtColor(original,cv2.COLOR_BGR2RGB))

  f.add_subplot(2,2,2)
  plt.title('Imagem transformada')
  plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))

  f.add_subplot(2,2,3)
  plt.title('Histograma da imagem original')
  plt.plot(cv2.calcHist([original],[0],None,[256],[0,255]))

  f.add_subplot(2,2,4)
  plt.title('Histograma da imagem transformada')
  plt.plot(cv2.calcHist([image],[0],None,[256],[0,255]))

  plt.show()
  
  return saveChanges(original, image)



def binarizar_gray(image, limiar = 100):

  '''
      Input: imagem - imagem em tons de cinza
             limiar - limiar da binarização, default = 100
      Output: None
  '''
  image[image<limiar] = 1
  image[image>=limiar] = 0
  
  lab1.viewImage(image)
  


def menu():
  choice = ''
  images = [None , None]
  names = ['', '']

  while(choice is not 'Q' and choice is not 'q'):
    print("************MENU**************")
    #time.sleep(1)
    print()
    choice = input("""
                      A: Carregar imagem
                      B: Exibir imagem
                      C: Salvar imagem
                      D: Exibir negativo
                      E: Equalizar histograma
                      F: Transformação de Intensidade Gray
                      G: Transformação de Potencia
                      H: Binarização de Imagem
                      Q: Sair

                      Imagens no sistema: %s

                      Opção: """ % str(names))

    if choice=="Q" or choice=="q":
        sys.exit

    elif choice == "A" or choice =="a":
      n = 1 - options(images, names, 'Qual das imagens deseja sobrescrever?')
      images[n], names[n] = lab1.loadImage()

    elif images[0] is None and images[1] is None:
      print('Nenhuma imagem no sistema')
      print('<Pressione ENTER para continuar>')
      input()
      
    elif choice == "B" or choice =="b":
      if images[1] is None:
        lab1.viewImage(images[0], names[0])
      elif images[0] is None:
        lab1.viewImage(images[1], names[1])
      else:
        lab1.viewImages(images, names)
      

    elif choice == "C" or choice =="c":
      n = options(images, names, 'Qual das imagens deseja salvar?')
      lab1.saveImage(images[n])


    elif choice=="D" or choice=="d":
      n = options(images, names, 'Qual das imagens será negativa?')
      images[n] = negative(images[n])


    elif choice=="E" or choice=="e":
      n = options(images, names, 'Qual das imagens será equalizada?')
      if len(images[n].shape) < 3:
        images[n] = equalizeHist_gray(images[n])
      else:
        images[n] = equalizeHist(images[n])


    elif choice=="F" or choice=="f":
      n = options(images, names, 'Qual das imagens será transformada (gray)?')
      mudar = input("Deseja mudar os intervalos e valores da transformada (s/n)? ")
      if mudar == 's' or mudar == 'S':
        a,b,alfa,beta,charlie = input("Qual é o valor do limiar (faixa de valores) 'a' e 'b', e quais os novos valores serão atribuídos aos intervalos 1, 2 e 3? [escrever em uma linha, separado por vírgula] ")
      images[n] = trans_intensidade_gray(images[n])
      

    elif choice=="G" or choice=="g":
      n = options(images, names, 'Qual das imagens será transformada?')
      images[n] = trans_potencia(images[n])
    
    
    elif choice=="H" or choice=="h":
      n = options(images, names, 'Qual das imagens será binarizada?')

      value = input('Limiar?  (0 < limiar < 255) :')
      value = int(value)

      if value > 0 and value < 255:
        images[n] = lab1.binarizar(images[n], value)
      
      #images[n] = binarizar_gray(images[n],float(limiar))
    

    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")



if __name__=="__main__":
  menu()

