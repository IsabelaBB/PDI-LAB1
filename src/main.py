#!/usr/bin/python3

import cv2
import numpy as np
import sys
import os
import matplotlib
from matplotlib import pyplot as plt
# Agg backend runs without a display
matplotlib.use( 'tkagg' )
from skimage.measure import compare_ssim
import lab1
from utils import options, saveChanges
import lab2


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
                      D: Exibir Histograms
                      E: Calcular imagem-diferença, erro médio quadrático e PSNR
                      F: Alterar a intensidade
                      G: Alterar o brilho
                      H: Fazer sub-amostragem
                      I: Binarizar
                      J: Negativo
                      K: Equalizar histograma
                      Q: Sair

                      Opção: """)

    if choice=="Q" or choice=="q":
        sys.exit

    elif choice == "A" or choice =="a":
      n = options(images, names, 'Qual das imagens deseja sobrescrever?')
      images[n], name[n] = lab1.loadImage()

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
      lab1.viewHistograms(images[0])
      lab1.viewHistograms(images[1])
      

    elif choice=="E" or choice=="e":
      option = 'A'
      if images[0] is None or images[1] is None:
        print('Sao necessarias duas imagens no sistema para calcular a diferenca')
        option = input('Deseja carregar outra imagem ? A:sim B:nao  :')

        if (option == 'A' or option == 'a') and images[0] is None:
          images[0], names[0] = lab1.loadImage()
        elif (option == 'A' or option == 'a') and images[1] is None:
          images[1], names[1] = lab1.loadImage()

      if (option == 'A' or option == 'a') and images[0] is not None and images[1] is not None:
        lab1.calImgDif(images[0], images[1])

    elif choice=="F" or choice=="f":
      n = options(images, names, 'Qual das imagens deseja alterar a intensidade?')
      
      value = 0
      print('(Utilize valor negativo para diminuir e positivo para aumentar)')
      value = input('A intensidade será alterada em quanto?  [-255,255] :')
      value = int(value)
      
      if value >= -255 and value <= 255:
        images[n] = lab1.itensidade(images[n], abs(value), (value>0))

    elif choice=="G" or choice=="g":
      n = options(images, names, 'Qual das imagens deseja alterar o brilho?')
      
      print('(Utilize valor negativo para diminuir e positivo para aumentar)')
      value = input('O brilho será alterado em quanto?  [-255,255] :')
      value = int(value)
      
      if value >= -255 and value <= 255:
        images[n] = lab1.brightness(images[n], abs(value), (value>0))

    elif choice=="H" or choice=="h":
      n = options(images, names, 'Qual das imagens deseja alterar a amostragem?')
      
      print(' O valor de amostragem, aqui, representa, aproximadamente, quantos pixels serão unidos em x e y.')
      print(' Este valor é aproximado porque as dimensoes da imagem podem não ser multiplas do valor da amostragem')
      value = input('A amostragem será alterado em quanto?  (0 < amostragem) :')
      value = int(value)

      if value > 0:
        images[n] = lab1.subamostragem(images[n], value)
    
    elif choice=='I' or choice=='i':
      n = options(images, names, 'Qual das imagens deseja alterar o limiar?')

      value = input('Limiar?  (0 < limiar < 255) :')
      value = int(value)

      if value > 0 and value < 255:
        images[n] = lab1.binarizar(images[n], value)
    
    
    elif choice=="J" or choice=="j":
      n = options(images, names, 'Qual das imagens será negativa?')
      images[n] = lab2.negative(images[n])
      

    elif choice=="K" or choice=="k":
      n = options(images, names, 'Qual das imagens será equalizada?')
      images[n] = lab2.equalizeHist_gray(images[n])

    
    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")


if __name__=="__main__":
  menu()