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
    mediana.append(cv2.medianBlur(img, i))
  
  for i in range(len(mascaras)):
    compare = np.concatenate((img, mediana[i]),axis=1) #side by side comparison
    title = ('original x mascara de mediana %d' %mascaras[i])
    cv2.imshow(title , compare)
    cv2.waitKey(0)
  cv2.destroyAllWindows()

def calcMaskMedianaUnico(img):
  mascara = int(input("Qual a mascara? ex.: 3 ou 5 ou 7 - APENAS valor ímpar > 3. \n --> "))
  #img = cv2.imread(image_name)  
  mediana = cv2.medianBlur(img, mascara)
  compare = np.concatenate((img, mediana),axis=1) #side by side comparison
  title = ('original x mascara de mediana %d' %mascara)
  cv2.imshow(title , compare)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  return saveChanges(image, mediana)

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
  
  print()
  #recebe a dimensao da mascara
  mascara = int(input("Qual a mascara? ex.: 3 ou 5 ou 7 - APENAS valor ímpar > 3. \n --> "))

  #opções de desvio
  option = int(input("""
                      1: Entrar com desvio de X e Y
                      2: Entrar apenas com desvio de X
                      Opção: """))
  if(option == 1):
    stdX = float(input("Qualo valor do desvio padrão de X ? "))
    stdY = float(input("Qualo valor do desvio padrão de Y ? "))
    #aplica a filtragem gaussiana
    gaussian = cv2.GaussianBlur(img,(mascara,mascara),stdX, stdY)
    
  elif(option == 2):
    stdX = int(input("Qualo valor do desvio padrão de X ? "))
     #aplica a filtragem gaussiana
    gaussian = cv2.GaussianBlur(img,(mascara,mascara),stdX)
  
  '''
  #concatena a imagem original com a imagem que passou pelo processo de filtragem
  compare = np.concatenate((img, gaussian),axis=1) 
  #define titulo da imagem 
  title = ('Imagem original x Imagem apos Filtro Gaussiano %d' %mascara)
  #plot image
  cv2.imshow(title , compare)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  '''

  lab1.viewImages([img, gaussian], ['Imagem original', 'Imagem apos Filtro Gaussiano %f' %mascara])
  return saveChanges(img, gaussian)
  

def sobel(img):
  
  #recebe a dimensao da mascara
  kernel = 0
  print()
  while(kernel is not 3 and kernel is not 5 and kernel is not 7):
    kernel = int(input('Tamanho do filtro? (3 ou 5 ou 7, apenas) : '))
    if kernel is not 3 and kernel is not 5 and kernel is not 7 :
      print('ERRO: O tamanho do filtro deve ser 3, 5 ou 7!')

  # converte a imagem para cinza, se ela ja não for
  if len(img.shape) > 2:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  else:
    gray = img

  # aplica o filtro sobel nas direcoes x e y
  grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel)
  grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel)  
  
  # o resultado de cada mascara do filtro possui valores float
  # pega o valor absoluto dos pixels resultantes do gradiente na direcao x e y
  abs_grad_x = cv2.convertScaleAbs(grad_x)
  abs_grad_y = cv2.convertScaleAbs(grad_y)
  
  # cv2.addWeighted(src1, alpha, src2, beta, gamma) -> src1 * alpha + src2 * beta + gamma
  # faz a soma dos grdientes x e y
  grad = cv2.addWeighted(grad_x, 0.5, grad_y, 0.5, 0) # gradiente com valores float. Os valores são deslocados para serem 8b
  grad_trunc = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0) # gradiente com valores absolutos

  # exibe as imagens
  lab1.viewImages([img, grad_trunc, grad], ['Imagem original', 'Sobel valores absolutos', 'Sobel valores deslocados'])

  return saveChanges(img,grad_trunc)



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
                      D: Filtro de Mediana 
                      E: Exibir múltiplos filtros de mediana
                      F: Filtro de Média 
                      G: Filtro Gaussiano
                      H: Filtro Sobel
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
      n = options(images, names, 'Qual das imagens será aplicado o filtro de mediana?')
      images[n] = calcMaskMedianaUnico(images[n])


    elif choice=="E" or choice=="e":
      n = options(images, names, 'Qual das imagens serão aplicados vários filtros de mediana para serem exibidos??')
      exibirMultiplasMaskMediana(images[n])


    elif choice=="F" or choice=="f":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de Média?')
      images[n] = calcMaskMedia(images[n])
      

    elif choice=="G" or choice=="g":
      n = options(images, names, 'Qual das imagens será aplicado o filtro Gaussiano?')
      images[n] = filterGaussian(images[n])
    

    elif choice=="H" or choice=="h":
      n = options(images, names, 'Qual das imagens será aplicado o filtro Sobel?')
      images[n] = sobel(images[n])


    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")



if __name__=="__main__":
  menu()

