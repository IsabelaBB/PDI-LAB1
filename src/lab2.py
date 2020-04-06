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

'''
TRABALHO EM GRUPO DE NO MÁXIMO 5 PESSOAS ENVIAR LINK PARA ACESSO A TODOS OS CÓDIGOS, 
ARQUIVO EXECUTÁVEL E EXPLICAÇÕES NECESSÁRIAS (incluindo instruções para instalar compiladores e bibliotecas). 
******************************************************************* 
Implementação em PHYTON, JAVA, C ou C++ de códigos para: 
- Operações de realce (transformações de intensidade), 
sendo, no mínimo: negativo, binarização e equalização de histogramas.
'''


# recebe uma imagem BGR, imprime o negativo da imagem
# e retorna uma imagem (original ou negativa)
def negative(image):
  im_neg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  im_neg = 255 - im_neg
  lab1.viewImage(im_neg, 'imagem negativa')
  return saveChanges(image, im_neg)



# Equalização de histograma
# com os tres canais de cores (resultado estranho)
def equalizeHist(image):
  if len(image.shape) < 3:
    print('Essa opção só é válida para imagens coloridas')
    print('<Pressione ENTER para continuar>')
    input()
    return image

  original = image
  
  # probabilidade
  p = [np.zeros(256), np.zeros(256), np.zeros(256)]

  # esse v_min é a intensidade mínima em cada canal de cor
  v_min = [256, 256, 256] # o valor real (da formula) de v_min é v[0][v_min[0]], por exemplo
  
  # probabilidade acumulada
  v = [np.zeros(256), np.zeros(256), np.zeros(256)]

  h, w, _ = image.shape

  # calcula valores de p e v_min
  for x in range(w):
    for y in range(h):
      if image[y,x,0] < v_min[0]:
        v_min[0] = image[y,x,0]

      if image[y,x,1] < v_min[1]:
        v_min[1] = image[y,x,1]

      if image[y,x,2] < v_min[2]:
        v_min[2] = image[y,x,2]

      p[0][image[y,x,0]] += 1
      p[1][image[y,x,1]] += 1
      p[2][image[y,x,2]] += 1
      
  # calcula valores de v
  v[0][0] = p[0][0]/(w*h)
  v[1][0] = p[1][0]/(w*h)
  v[2][0] = p[2][0]/(w*h)
  for i in range(255):
    i += 1
    v[0][i] = v[0][i-1] + p[0][i]/(w*h)
    v[1][i] = v[1][i-1] + p[1][i]/(w*h)
    v[2][i] = v[2][i-1] + p[2][i]/(w*h)

  '''
  # visualizar valores em p
  plt.plot(p[0],color='red'), plt.title('Histograma P')
  plt.plot(p[1],color='green')
  plt.plot(p[2],color='blue')
  plt.xlim([0,255])
  plt.show()

  # visualizar valores em v
  plt.plot(v[0], color='red'), plt.title('Histograma V')
  plt.plot(v[1], color='green')
  plt.plot(v[2], color='blue')
  plt.xlim([0,255])
  plt.show()
  '''

  # atualiza os valores da imagem (valores v*)
  for x in range(w):
    for y in range(h):
      image[y,x,0] = int((v[0][image[y,x,0]] - v[0][v_min[0]]) / (1 - v[0][v_min[0]])*255 +0.5)
      image[y,x,1] = int((v[1][image[y,x,1]] - v[1][v_min[1]]) / (1 - v[1][v_min[1]])*255 +0.5)
      image[y,x,2] = int((v[2][image[y,x,2]] - v[2][v_min[2]]) / (1 - v[2][v_min[2]])*255 +0.5)

  '''
  print('v=')
  for i in range(256):
    print(str(v[0][i]) + ' ' + str(v[1][i]) + ' ' + str(v[2][i]))

  print('')
  for i in range(256):
    print(str(p[0][i]) + ' ' + str(p[1][i]) + ' ' + str(p[2][i]))
  '''

  '''
  # equalizacao automatica do opencv (para comparacao)
  equ = cv2.equalizeHist(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
  lab1.viewImage(equ, 'resultado da equalização2')
  lab1.viewHistograms(equ)
  '''

  # exibe
  lab1.viewImage(image, 'resultado da equalização')
  lab1.viewHistograms(image)

  return saveChanges(original, image)



# Equalização de histograma
# recebe uma imagem BGR
def equalizeHist_gray(image):
  original = image

  if len(image.shape) > 2:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

  '''
  # visualizar valores em p
  plt.plot(p,color='black'), plt.title('Histograma P')
  plt.xlim([0,255])
  plt.show()

  # visualizar valores em v
  plt.plot(v,color='black'), plt.title('Histograma V')
  plt.xlim([0,255])
  plt.show()
  '''

  # atualiza os valores da imagem (valores v*)
  for x in range(w):
    for y in range(h):
      image[y,x] = int((v[image[y,x]] - v[v_min]) / (1 - v[v_min])*255 +0.5)

  '''
  print('v=')
  for i in range(256):
    print(str(v[i]))

  print('')
  for i in range(256):
    print(str(p[i]))
  '''

  '''
  # equalizacao automatica do opencv (para comparacao)
  equ = cv2.equalizeHist(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
  lab1.viewImage(equ, 'resultado da equalização2')
  lab1.viewHistograms(equ)
  '''

  # exibe
  lab1.viewHistograms(image)
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
  return saveChanges(original, image)

def trans_potencia(image):
  original = image
  c = 1
  gamma = 2.5
  
  altura = original.shape[0]
  largura = original.shape[1]
  
  if len(original.shape) > 2 :
    dimensoes = original.shape[2]    
    image = np.zeros((altura,largura,dimensoes),dtype=np.float32)
    
    for i in range(altura):
        for j in range(largura):
            for k in range(dimensoes):
              image[i,j,k] = c*math.pow(original[i, j, k], gamma)
            
    
  else:
    image = np.zeros((altura,largura,1),dtype=np.float32)
    
    for i in range(altura):
        for j in range(largura):
              image[i,j] = c*math.pow(original[i, j], gamma)
              
  cv2.normalize(image,image,0,255,cv2.NORM_MINMAX)
  image = cv2.convertScaleAbs(image)
  lab1.viewImage(image);

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
                      H: 
                      I: 
                      Q: Sair

                      Opção: """)

    if choice=="Q" or choice=="q":
        sys.exit

    elif choice == "A" or choice =="a":
      n = options(images, names, 'Qual das imagens deseja sobrescrever?')
      images[n], names[n] = lab1.loadImage()

    elif images[0] is None and images[1] is None:
      print('Nenhuma imagem no sistema')
      print('<Pressione ENTER para continuar>')
      input()
      
    elif choice == "B" or choice =="b":
      n = options(images, names, 'Qual das imagens deseja visualizar?')
      lab1.viewImage(images[n])
      

    elif choice == "C" or choice =="c":
      n = options(images, names, 'Qual das imagens deseja salvar?')
      lab1.saveImage(images[n])


    elif choice=="D" or choice=="d":
      n = options(images, names, 'Qual das imagens será negativa?')
      images[n] = negative(images[n])
      

    elif choice=="E" or choice=="e":
      n = options(images, names, 'Qual das imagens será equalizada?')
      images[n] = equalizeHist_gray(images[n])

    elif choice=="F" or choice=="f":
      n = options(images, names, 'Qual das imagens será transformada (gray)?')
      mudar = input("Deseja mudar os intervalos e valores da transformada (s/n)? ")
      if mudar == 's' or mudar == 'S':
        a,b,alfa,beta,charlie = input("Qual é o valor do limiar (faixa de valores) 'a' e 'b', e quais os novos valores serão atribuídos aos intervalos 1, 2 e 3? [escrever em uma linha, separado por vírgula] ")
      images[n] = trans_intensidade_gray(images[n])
      
    elif choice=="G" or choice=="g":
      n = options(images, names, 'Qual das imagens será transformada?')
      images[n] = trans_potencia(images[n])
      
    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")


if __name__=="__main__":
  import lab1
  menu()

