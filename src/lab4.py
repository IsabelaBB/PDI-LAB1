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

TRABALHO EM GRUPO DE NO MÁXIMO 5 PESSOAS ENVIAR LINK PARA ACESSO A TODOS OS CÓDIGOS, ARQUIVO EXECUTÁVEL E EXPLICAÇÕES 
NECESSÁRIAS (incluindo instruções para instalar compiladores e bibliotecas). 
******************************************************************* 
Implementação em PHYTON, JAVA, C ou C++ de códigos para: - Operações de filtragem espacial - Filtros 
morfológicos (erosão e dilatação, sendo que o tamanho e o formato da máscara - retangular ou cruz - são parâmetros de entrada) 


def exibirMultiplasMaskMedia(img):
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
    title = ('original x mascara de media %d' %mascaras[i])
    cv2.imshow(title , compare)
    cv2.waitKey(0)
  cv2.destroyAllWindows()

def calcMaskMediaUnico(img):
  mascara = int(input("Qual a mascara? ex.: 3 ou 5 ou 7 - APENAS valor ímpar > 3. \n --> "))
  #img = cv2.imread(image_name)  
  media = cv2.medianBlur(img, mascara)
  compare = np.concatenate((img, media),axis=1) #side by side comparison
  title = ('original x mascara de media %d' %mascara)
  cv2.imshow(title , compare)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  return media

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
                      D: Filtro de média 
                      E: Exibir múltiplos filtros de média
                      F: 
                      G: 
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
      n = options(images, names, 'Qual das imagens será aplicado o filtro de média?')
      images[n] = calcMaskMediaUnico(images[n])

    elif choice=="E" or choice=="e":
      n = options(images, names, 'Qual das imagens serão aplicados vários filtros de média para serem exibidos??')
      exibirMultiplasMaskMedia(images[n])


    elif choice=="F" or choice=="f":
      
      

    elif choice=="G" or choice=="g":
      
    
    
    elif choice=="H" or choice=="h":

    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")



if __name__=="__main__":
  menu()

