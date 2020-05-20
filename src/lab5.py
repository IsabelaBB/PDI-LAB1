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
import lab4

'''
TRABALHO EM GRUPO DE NO MÁXIMO 5 PESSOAS ENVIAR LINK PARA ACESSO A TODOS OS CÓDIGOS,
ARQUIVO EXECUTÁVEL E EXPLICAÇÕES NECESSÁRIAS (incluindo instruções para instalar compiladores e bibliotecas).
*******************************************************************
Implementação em PHYTON, JAVA, C ou C++ de códigos para:
- Segmentação de imagens:
  - Detecção de descontinuidades seguida de limiarização
  - Transformada de Hough (linhas e círculos)
  - K-means para segmentação de imagens coloridas e em tons de cinza
'''

def houghLinhas (image,threshold):

  img = np.copy(image)
  
  #Detecção das bordas usando detector Canny
  edges = cv2.Canny(image,50,200,apertureSize = 3)

  #Aplicação da transformada
  #  - Saída do detector de bordas
  #  - Parametro rô (rho)
  #  - Parametro teta (theta)
  #  - Limiar
  lines = cv2.HoughLines(edges,1,np.pi/180,threshold)

  #Desenhando linhas encontradas
  for i in range(0, len(lines)):
    rho = lines[i][0][0]
    theta = lines[i][0][1]
    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    cv2.line(image, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

  #visualizacao do resultado
  lab1.viewImages([img, image], ['Imagem original', 'Transformada de Hough'])
  return saveChanges(img,image)


def houghCirculos(image,minRadius,maxRadius):

  output = np.copy(image)

  #escala de cinza
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  #suavizacao para reduzir ruido e
  #diminuir deteccao de ciruculos falsos
  gray = cv2.medianBlur(gray, 5)    
    
  rows = gray.shape[0]

  #Aplicação da transformada
  #  - Imagem em tonsde cinza
  #  - Metodo de deteccao
  #  - 
  #  - Distancia minima entre os centros
  #  - Limiar superior
  #  - Limiar para detecacao de centro
  #  - Raio minimo
  #  - Raio maximo
  circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=30,
                               minRadius=minRadius,
                               maxRadius=maxRadius)

  #Desenhando circulos encontrados
  if circles is not None:

    circles = np.uint16(np.around(circles))

    for i in circles[0, :]:
      center = (i[0], i[1])
      # circle center
      cv2.circle(output, center, 1, (0, 100, 100), 3)
      # circle outline
      radius = i[2]
      cv2.circle(output, center, radius, (255, 0, 255), 3)

  #visualizacao do resultado
  lab1.viewImages([image, output], ['Imagem original', 'Transformada de Hough'])
  return saveChanges(image,output)
  
def menu():
  choice = ''
  images = [None , None]
  names = ['', '']

  while(choice != 'Q' and choice != 'q'):
    print("************MENU**************")
    #time.sleep(1)
    print()
    choice = input("""
                      A: Carregar imagem
                      B: Exibir imagem
                      C: Salvar imagem
                      D: Detecção de descontinuidades e limiarização 
                      E: Transformada de Hough (linhas)
                      F: Transformada de Hough (círculos)
                      G: K-means
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

    elif choice=="E" or choice=="e":
      n = options(images, names, 'Qual das imagens será aplicado a Transformada de Hough?')
      print("Transformada de Hough(linhas)\n")
      limiar = int(input("Qual o valor do limiar?"))
      images[n] = houghLinhas(images[n],limiar)


    elif choice=="F" or choice=="f":
      n = options(images, names, 'Qual das imagens será aplicado a Transformada de Hough?')
      print("Transformada de Hough(circulos)\n")
      raioMin = int(input("Qual o valor do raio minimo? (recomendado: 1)"))
      raioMax = int(input("Qual o valor do raio maximo? (recomendado: 50)"))
      images[n] = houghCirculos(images[n], raioMin, raioMax)

    elif choice=="G" or choice=="g":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de dilatação?')    
      
    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")



if __name__=="__main__":
  menu()
