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
Implementação em PHYTON, JAVA, C ou C++ de códigos para: - Operações de filtragem espacial - Filtros 
morfológicos (erosão e dilatação, sendo que o tamanho e o formato da máscara - retangular ou cruz - são parâmetros de entrada) 
'''

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
      n = options(images, names, 'Qual das imagens será aplicado o filtro de erosão?')
      mask = int(input("Qual o tamanho da máscara? ex.: 5 - vai ser uma máscara 5x5 \n -->"))
      mask = (mask, mask)
      tipo = -1
      tipo = int(input("Qual o formato da máscara? 0: retangular; 1: elíptica; 2:cruz. \n -->"))
      
      images[n] = erosao(images[n], mask, tipo)

    elif choice=="E" or choice=="e":
      n = options(images, names, 'Qual das imagens será aplicado o filtro de dilatação?')
      mask = int(input("Qual o tamanho da máscara? ex.: 5 - vai ser uma máscara 5x5 \n -->"))
      mask = (mask, mask)
      tipo = -1
      tipo = int(input("Qual o formato da máscara? 0: retangular; 1: elíptica; 2:cruz. \n -->"))
      
      images[n] = erosao(images[n], mask, tipo)


    elif choice=="F" or choice=="f":
      
      

    elif choice=="G" or choice=="g":
      
    
    
    elif choice=="H" or choice=="h":

    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")



if __name__=="__main__":
  menu()

