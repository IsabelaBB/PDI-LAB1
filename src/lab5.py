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
  output = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

  #Aplicação da transformada
  #  - Saída do detector de bordas
  #  - Parametro rô (rho)
  #  - Parametro teta (theta)
  #  - Limiar
  lines = cv2.HoughLines(edges,1,np.pi/180,threshold)
  
  for i in range(0, len(lines)):
    rho = lines[i][0][0]
    theta = lines[i][0][1]
    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    cv2.line(output, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

  lab1.viewImages([img, output], ['Imagem original', 'Transformada de Hough'])
  return saveChanges(image,output)

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
      n = options(images, names, 'Qual das imagens será aplicado o filtro de dilatação?')

    elif choice=="G" or choice=="g":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de dilatação?')    
    elif choice=="H" or choice=="h":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de Canny?')
      
    elif choice=="I" or choice=="i":
      n = options(images, names, 'Qual das imagens será aplicado o filtro bilateral?')
      
    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")



if __name__=="__main__":
  menu()
