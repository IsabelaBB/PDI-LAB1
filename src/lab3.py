#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

'''
TRABALHO EM GRUPO DE NO MÁXIMO 5 PESSOAS ENVIAR LINK PARA ACESSO A TODOS OS CÓDIGOS, 
ARQUIVO EXECUTÁVEL E EXPLICAÇÕES NECESSÁRIAS (incluindo instruções para instalar compiladores e bibliotecas). 
******************************************************************* 
Implementação em PHYTON, JAVA, C ou C++ de códigos para: 
- Operações de filtragem espacial - FPB (média, gaussiano e mediana, com tamanho da janela e desvio padrão da guaussiana sendo
parâmetros de entrada) - FBA (laplaciano e sobel) 
'''

def exibirMultiplasMaskMediana(img):
  #img = cv2.imread(image_name)  
  mascaras=[]
  median = []
  new_mask=[]
  print("\nInstrução: aperte uma tecla para ir p/ próxima imagem. Depois que todas forem exibidas, apertar uma tecla novamente irá finalizar a execução deste código.")
  mascaras = input("Quais as mascaras? ex.: 3 5 7 - APENAS valores ímpares > 3. \n --> ").split()
  #mascaras  = "-1 1 3 1 5 7 8".split()
  mascaras = list(map(int,mascaras))
  #print(mascaras)
  for i in mascaras:  
    if i>=3 and i%2 != 0:
   #   print(i)
      new_mask.append(i)
    mascaras = new_mask 
  
  for i in mascaras:  #valores impares para a mascara
    median.append(cv2.medianBlur(img, i))
  
  for i in range(len(mascaras)):
    compare = np.concatenate((img, median[i]),axis=1) #side by side comparison
    title = ('original x mascara de mediana %d' %mascaras[i])
    cv2.imshow(title , compare)
    cv2.waitKey(0)
  cv2.destroyAllWindows()

def calcMaskMedianaUnico(img):
  mascara = int(input("Qual a mascara? ex.: 3 ou 5 ou 7 - APENAS valor ímpar > 3. \n --> "))
  #img = cv2.imread(image_name)  
  media = cv2.medianBlur(img, mascara)
  compare = np.concatenate((img, media),axis=1) #side by side comparison
  title = ('original x mascara de mediana %d' %mascara)
  cv2.imshow(title , compare)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  return media

def calcMaskMedia(img):
  mascara = int(input("Qual a mascara? ex.: 3 ou 5 ou 7 - APENAS valor ímpar > 3. \n --> "))
  #img = cv2.imread(image_name)  
  media = cv2.blur(img, (mascara,mascara))
  compare = np.concatenate((img, media),axis=1) #side by side comparison
  title = ('original x mascara de media %d' %mascara)
  cv2.imshow(title , compare)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  return media
  
def filterGaussian(img):
  
  '''
    Input: img - imagem; 
           sigmaX - desvio padrão na direção x
           sigmaY - desvio padrão na direção y
           
           Obs.: Se apenas o sigmaX for especificado, o sigmaY será considerado igual ao sigmaX.
                 Pelo menos o sigmaX deve, obrigatoriamente, ser especificado.
    Output: None
  '''
    
  #recebe a dimensao da mascara
  mascara = int(input("Qual a mascara? ex.: 3 ou 5 ou 7 - APENAS valor ímpar > 3. \n --> "))

  #opções de desvio
  option = int(input("""
                      1: Entrar com desvio de X e Y
                      2: Entrar apenas com desvio de X
                      Opção: """))
  if(option == 1):
    stdX = int(input("Qualo valor do desvio padrão de X ?"))
    stdY = int(input("Qualo valor do desvio padrão de Y ?"))
    #aplica a filtragem gaussiana
    gaussian = cv2.GaussianBlur(img,(mascara,mascara),stdX, stdY)
    
  elif(option == 2):
    stdX = int(input("Qualo valor do desvio padrão de X ?"))
     #aplica a filtragem gaussiana
    gaussian = cv2.GaussianBlur(img,(mascara,mascara),stdX)
  
  
  #concatena a imagem original com a imagem que passou pelo processo de filtragem
  compare = np.concatenate((img, gaussian),axis=1) 
  #define titulo da imagem 
  title = ('Imagem original x Imagem apos Filtro Gaussiano %d' %mascara)
  #plot image
  cv2.imshow(title , compare)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  


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
                      D: Filtro de mediana 
                      E: Exibir múltiplos filtros de mediana
                      F: Filtro de média 
                      G: Filtro Gaussiano
                      H: 
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
      lab1.viewImage(images[n], names[n])
      

    elif choice == "C" or choice =="c":
      n = options(images, names, 'Qual das imagens deseja salvar?')
      lab1.saveImage(images[n])

    elif choice=="D" or choice=="d":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de mediana?')
      images[n] = calcMaskMedianaUnico(images[n])

    elif choice=="E" or choice=="e":
      n = options(images, names, 'Qual das imagens serão aplicados vários filtros de mediana para serem exibidos??')
      exibirMultiplasMaskMediana(images[n])


    elif choice=="F" or choice=="f":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de média?')
      images[n] = calcMaskMedia(images[n])
      

    elif choice=="G" or choice=="g":
      n = options(images, names, 'Qual das imagens será aplicado o filtro Gaussiano?')
      filterGaussian(images[n])
    
    #elif choice=="H" or choice=="h":

    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")



if __name__=="__main__":
  menu()

