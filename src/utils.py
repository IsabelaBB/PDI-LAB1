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

'''
Este arquivo contém funções de uso geral
'''


# Se há duas imagens no sistema, exibe uma mensagem e recebe A ou B
# retorna: o indice da imagem "ocupada" (caso só tenha uma imagem)
#          ou o indice da imagem que o usuário escolheu
#          ou o indice 0, se não há imagens (cai apenas no caso de chamar loadImage)
def options(images, names, msg):
  opt = ''
  if images[0] is not None and images[1] is not None:
    opt = input(msg + ' A:'+names[0]+' B:'+names[1]+' :')
  if images[1] is None or opt == 'A' or opt == 'a':
      return 0
  elif images[0] is None or opt == 'B' or opt == 'b':
      return 1 
  else: 
    return 1



# teste não usado
def options_bkp(images, names, function, args):
  opt = ''
  if images[0] is not None and images[1] is not None:
    opt = input('Qual das imagens deseja sobrescrever? A:'+names[0]+' B:'+names[1]+' :')
  if images[0] is None or opt == 'A' or opt == 'a':
    images[0], names[0] = function(args)
  elif images[0] is None or opt == 'B' or opt == 'b':
    images[1], names[1] = function(args)
  return images



# opção de manter no sistema as modificações feitas
def saveChanges(image, imageChanged):
  print()
  opt = input('Deseja guardar a alteração? Y:sim  N:não   :')
  if opt == 'Y' or opt == 'y':
    return imageChanged
  else:
    return image