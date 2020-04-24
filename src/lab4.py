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
import lab2
import lab3

'''
TRABALHO EM GRUPO DE NO MÁXIMO 5 PESSOAS ENVIAR LINK PARA ACESSO A TODOS OS CÓDIGOS, ARQUIVO EXECUTÁVEL E EXPLICAÇÕES 
NECESSÁRIAS (incluindo instruções para instalar compiladores e bibliotecas). 
******************************************************************* 
Implementação em PHYTON, JAVA, C ou C++ de códigos para: 
- Operações de filtragem espacial 
- Filtros morfológicos (erosão e dilatação, sendo que o tamanho e o formato da máscara - retangular ou cruz - são parâmetros de entrada) 
'''


def erosao(image, mask, tipo):
  #print("tipo: ", tipo)
  kernel = None
  while(tipo < 0 or tipo > 2):
    if tipo == 0:
      # Rectangular Kernel
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT,mask)
    elif tipo == 1:
      # Elliptical Kernel
      kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,mask)
    elif tipo == 2:
      # Cross-shaped Kernel
      kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,mask)
    else:
      print("Tipo inválido !")
      tipo = int(input("Qual o formato da máscara? 0: retangular; 1: elíptica; 2:cruz. \n -->"))
  
  erosion = cv2.erode(image,kernel,iterations = 1)

  title = ('original x erosao [clique nesta janela e aperte uma tecla para sair]')
  compare = np.concatenate((image, erosion),axis=1)
  cv2.imshow(title , compare)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  return saveChanges(image, erosion)


def dilatar(image, mask, tipo):
  kernel = None
  while(tipo < 0 or tipo > 2):
    if tipo == 0:
      # Rectangular Kernel
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT,mask)
    elif tipo == 1:
      # Elliptical Kernel
      kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,mask)
    elif tipo == 2:
      # Cross-shaped Kernel
      kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,mask)
    else:
      print("Tipo inválido !")
      tipo = int(input("Qual o formato da máscara? 0: retangular; 1: elíptica; 2:cruz. \n -->"))

  dilation = cv2.dilate(image,kernel,iterations = 1)

  title = ('original x dilatacao [clique nesta janela e aperte uma tecla para sair]')
  compare = np.concatenate((image, dilation),axis=1)
  cv2.imshow(title , compare)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  return saveChanges(image, dilation)


def prewitt(image):
  # converte a imagem para cinza, se ela ja não for
  if len(image.shape) > 2:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  else:
    gray = image

  # cria as máscaras
  kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]], dtype=np.float32)
  kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]], dtype=np.float32)

  # aplica o filtro prewitt nas direcoes x e y
  grad_x = cv2.filter2D(gray, -1, kernelx)
  grad_y = cv2.filter2D(gray, -1, kernely)

  # o resultado de cada mascara do filtro possui valores float
  # pega o valor absoluto dos pixels resultantes do gradiente na direcao x e y
  abs_grad_x = cv2.convertScaleAbs(grad_x)
  abs_grad_y = cv2.convertScaleAbs(grad_y)
  
  # cv2.addWeighted(src1, alpha, src2, beta, gamma) -> src1 * alpha + src2 * beta + gamma
  # faz a soma dos grdientes x e y
  grad = cv2.addWeighted(grad_x, 0.5, grad_y, 0.5, 0) # gradiente com valores float. Os valores são deslocados para serem 8b

  # exibe as imagens
  lab1.viewImages([image, grad], ['Imagem original', 'Prewitt valores absolutos'])
  return saveChanges(image,grad)


def kirsch(image):
  # converte a imagem para cinza, se ela ja não for
  if len(image.shape) > 2:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  else:
    gray = image

  # cria as 8 máscaras
  kernelG1 = np.array([[ 5, -3, -3],
                      [ 5,  0, -3],
                      [ 5, -3, -3]], dtype=np.float32)

  kernelG2 = np.array([[-3, -3, -3],
                      [ 5,  0, -3],
                      [ 5,  5, -3]], dtype=np.float32)

  kernelG3 = np.array([[-3, -3, -3],
                      [-3,  0, -3],
                      [ 5,  5, 5]], dtype=np.float32)

  kernelG4 = np.array([[-3, -3, -3],
                      [-3,  0,  5],
                      [-3,  5,  5]], dtype=np.float32)

  kernelG5 = np.array([[-3, -3, 5],
                      [-3,  0, 5],
                      [-3, -3, 5]], dtype=np.float32)

  kernelG6 = np.array([[-3,  5,  5],
                      [-3,  0,  5],
                      [-3, -3, -3]], dtype=np.float32)

  kernelG7 = np.array([[ 5,  5,  5],
                      [-3,  0, -3],
                      [-3, -3, -3]], dtype=np.float32)

  kernelG8 = np.array([[ 5,  5, -3],
                      [ 5,  0, -3],
                      [-3, -3, -3]], dtype=np.float32)

  # aplica as 8 máscaras do filtro kirsc
  norm = cv2.NORM_MINMAX
  g1 = cv2.normalize(cv2.filter2D(gray, cv2.CV_32F, kernelG1), None, 0, 255, norm, cv2.CV_8UC1)
  g2 = cv2.normalize(cv2.filter2D(gray, cv2.CV_32F, kernelG2), None, 0, 255, norm, cv2.CV_8UC1)
  g3 = cv2.normalize(cv2.filter2D(gray, cv2.CV_32F, kernelG3), None, 0, 255, norm, cv2.CV_8UC1)
  g4 = cv2.normalize(cv2.filter2D(gray, cv2.CV_32F, kernelG4), None, 0, 255, norm, cv2.CV_8UC1)
  g5 = cv2.normalize(cv2.filter2D(gray, cv2.CV_32F, kernelG5), None, 0, 255, norm, cv2.CV_8UC1)
  g6 = cv2.normalize(cv2.filter2D(gray, cv2.CV_32F, kernelG6), None, 0, 255, norm, cv2.CV_8UC1)
  g7 = cv2.normalize(cv2.filter2D(gray, cv2.CV_32F, kernelG7), None, 0, 255, norm, cv2.CV_8UC1)
  g8 = cv2.normalize(cv2.filter2D(gray, cv2.CV_32F, kernelG8), None, 0, 255, norm, cv2.CV_8UC1)

  # pega os valores máximos de cada resultado
  grad = cv2.max(g1, g2)
  grad = cv2.max(grad, g3)
  grad = cv2.max(grad, g4)
  grad = cv2.max(grad, g5)
  grad = cv2.max(grad, g6)
  grad = cv2.max(grad, g7)
  grad = cv2.max(grad, g8)
  
  # exibe as imagens
  lab1.viewImages([image, grad], ['Imagem original', 'Kirsch valores absolutos'])
  return saveChanges(image,grad)



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
                      D: Filtro morfológico de erosão 
                      E: Filtro morfológico de dilatação
                      F: Filtro Prewitt
                      G: Filtro Kirsch
                      H: 
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
      
      n = options(images, names, 'Qual das imagens será aplicado o filtro de erosão?')
      print("Erosão\n")
      mask = int(input("Qual o tamanho da máscara? ex.: 5 - vai ser uma máscara 5x5 \n -->"))
      mask = (mask, mask)
      tipo = -1
      tipo = int(input("Qual o formato da máscara? 0: retangular; 1: elíptica; 2:cruz. \n -->"))
      images[n] = erosao(images[n], mask, tipo)

    elif choice=="E" or choice=="e":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de dilatação?')
      print("Dilatação\n")
      mask = int(input("Qual o tamanho da máscara? ex.: 5 - vai ser uma máscara 5x5 \n -->"))
      mask = (mask, mask)
      tipo = -1
      tipo = int(input("Qual o formato da máscara? 0: retangular; 1: elíptica; 2:cruz. \n -->"))
      
      images[n] = dilatar(images[n], mask, tipo)


    elif choice=="F" or choice=="f":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de dilatação?')
      images[n] = prewitt(images[n])

    elif choice=="G" or choice=="g":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de dilatação?')
      images[n] = kirsch(images[n])
    
    elif choice=="H" or choice=="h":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de dilatação?')
      
    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")



if __name__=="__main__":
  menu()

