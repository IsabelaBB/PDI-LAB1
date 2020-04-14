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
from utils import options, saveChanges

'''
TRABALHO LAB1 PDI

TRABALHO EM GRUPO DE NO MÁXIMO 5 PESSOAS Implementação em PHYTON, JAVA, C ou C++ de códigos para: 
- Ler arquivos de imagem acromáticas e de imagens coloridas, em qualquer padrão (jpg, eps, bmp, png etc) 
- Visualizar arquivos de imagem acromáticas e de imagens coloridas 
- Salvar arquivos de imagem acromáticas e de imagens coloridas em padrões específicos (jpg, bmp e png) 
- Calcular e visualizar o(s) histograma(s) de imagem acromáticas e de imagens coloridas 
(opção de visualizar a imagem à esquerda, o histograma à direita) 
- A partir de arquivos de imagens coloridas, separar as componentes R, G e B, para posterior processamento 
- Calcular a imagem-diferença entre duas imagens acromáticas 
- Calcular as métricas ERRO MÉDIO QUADRÁTICO e PSNR a partir da imagem-diferença. 
obs.: Opcionalmente, poderão ser usadas bibliotecas de processamento de imagens, como OpenCV.

Os códigos deverão ser compilados e mostrados em sala no dia da apresentação do trabalho final.
'''


# - Ler arquivos de imagem acromáticas e de imagens coloridas, em qualquer padrão (jpg, eps, bmp, png etc) 
def loadImage():
  print()
  filename = input('Filename: ')
  if not(os.path.exists(filename)) or not(os.path.isfile(filename)):
    print('ERRO: Imagem não encontrada')
    print('<Pressione ENTER para continuar>')
    input()
    return None, ''
  image = cv2.imread(filename)
  if image is not None:
    return image, filename.split('/')[-1]
  print('ERRO: Ocorreu um erro ao abrir a imagem')
  print('<Pressione ENTER para continuar>')
  input()
  return None,''


# - Visualizar arquivos de imagem acromáticas e de imagens coloridas 
def viewImages(images, titles=['image']):
  f = plt.figure()
  i = 1

  for image in images:
    title = titles[i-1]
    f.add_subplot(1,len(images),i)
    plt.title(title)
    if len(image.shape) > 2: # imagem é colorida
      plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    else: # imagem está em escala de cinza
      plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.01, hspace=0.01)
    i = i + 1
  
  plt.show()



# - Visualizar arquivos de imagem acromáticas e de imagens coloridas 
def viewImage(image, title='image'):
  #h, w, c = image.shape
  if len(image.shape) > 2:
    # imagem é colorida
    plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
  else:
    # imagem está em escala de cinza
    plt.imshow(image, cmap='gray')
  
  plt.axis('off')
  plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.01, hspace=0.01)

  plt.title(title)
  plt.show()
  

# - Salvar arquivos de imagem acromáticas e de imagens coloridas em padrões específicos (jpg, bmp e png) 
def saveImage(image):
  print()
  filename = input('Digite o diretorio/arquivo onde quer salvar: ')
  cv2.imwrite(filename,image)


# - Calcular e visualizar o(s) histograma(s) de imagem acromáticas e de imagens coloridas 
# (opção de visualizar a imagem à esquerda, o histograma à direita) 
# - A partir de arquivos de imagens coloridas, separar as componentes R, G e B, para posterior processamento 
def viewHistograms(image):
  # se as imagens já forem cinza, a conversão gera um erro
  if image is not None:
    # imagem cinza
    if len(image.shape) == 2:
      GR = cv2.calcHist([image],[0],None,[256],[0,255])

      plt.subplot(121), plt.imshow(image, cmap='gray', vmin=0, vmax=255), plt.title('Imagem cinza')
      plt.subplot(122), plt.plot(GR, color='gray'), plt.title('Histograma da imagem cinza')

      plt.xlim([0,255])
      plt.show()

    # imagem colorida
    else:
      image1 = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
      gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

      R = cv2.calcHist([image],[0],None,[256],[0,255])
      G = cv2.calcHist([image],[1],None,[256],[0,255])
      B = cv2.calcHist([image],[2],None,[256],[0,255])
      GR = cv2.calcHist([gray],[0],None,[256],[0,255])

      #plt.subplot(212), plt.plot(R,color='red'), plt.plot(G,color='green'), plt.plot(B,color='blue'), plt.plot(gray,color='gray'), plt.title('Histogramas')
      plt.subplot(241), plt.imshow(image[:,:,0], cmap='gray', vmin=0, vmax=255), plt.title('Componente RED')
      plt.subplot(242), plt.imshow(image[:,:,1], cmap='gray', vmin=0, vmax=255), plt.title('Componente GREEN')
      plt.subplot(243), plt.imshow(image[:,:,2], cmap='gray', vmin=0, vmax=255), plt.title('Componente BLUE')
      plt.subplot(244), plt.imshow(gray, cmap='gray', vmin=0, vmax=255), plt.title('Imagem cinza')
      
      plt.subplot(245), plt.plot(R,color='red'), plt.title('Histograma RED')
      plt.subplot(246), plt.plot(G,color='green'), plt.title('Histograma GREEN')
      plt.subplot(247), plt.plot(B,color='blue'), plt.title('Hisograma BLUE')
      plt.subplot(248), plt.plot(GR, color='gray'), plt.title('Histograma da imagem cinza')

      plt.xlim([0,255])
      plt.show()



# - Calcular a imagem-diferença entre duas imagens acromáticas 
# - Calcular as métricas ERRO MÉDIO QUADRÁTICO e PSNR a partir da imagem-diferença.
def calImgDif(image1, image2):
  # se as imagens já forem cinza, a conversão gera um erro
  if len(image1.shape) > 2:
    image1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)

  if len(image2.shape) > 2:
    image2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)

  print('image1 = '+str(image1.shape))
  print('image2 = '+str(image2.shape))
  print('..')

  # imagens com tamanhos diferentes precisam ser redimensionadas para o mesmo tamanho, ou também irá gerar erro
  if image1.size > image2.size:
    image1 = cv2.resize(image1,(image2.shape[1], image2.shape[0]))
    print('image1 = '+str(image1.shape))
  elif image1.size < image2.size:
    image2 = cv2.resize(image2,(image1.shape[1], image1.shape[0]))
    print('image2 = '+str(image2.shape))

  (score, diff) = compare_ssim(image1, image2, full=True)
  diff = (diff * 255).astype("uint8")
  
  print('Erro médio quadrático: '+str(np.square(diff).mean())+', PSNR: '+str(cv2.PSNR(image1, image2)))
  print('<Pressione ENTER para continuar>')
  viewImage(diff, 'Imagem diferença')
  input()
  
  #plt.imshow(diff, cmap='gray')
  #plt.title('Erro médio quadrático: '+str(np.square(diff).mean())+', PSNR: '+str(cv2.PSNR(image1, image2)))
  #plt.show()


def itensidade(img, value, option = True):
    
  '''
  Inputs:
  - img = Imagem BGR;
  - value = valor de ajuste de intensidade;
  - option = True: aumentar 
            False: diminuir
    Output: Salva imagem no diretório
  '''
  
  if len(img.shape) > 2:
      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  else:
    img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

  h, s, v = cv2.split(hsv)

  if(option == True):
    lim = 255 - value
    s[s > lim] = 255
    s[s <= lim] += value
    i = 'aumentou'
  elif(option == False):
    lim = 0 + value
    s[s<lim] = 0
    s[s>=lim] -= value
    i = 'diminuiu'

  final_hsv = cv2.merge((h, s, v))
  img2 = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
  viewImage(img2, 'Intensidade %s em %d' % (i,value))

  return saveChanges(img, img2)
    

def brightness(img, value, option = True):
    
    '''
        Inputs:
                - img = Imagem BGR;
                - value = valor de ajuste de brilho;
                - option = True: aumentar de brilho
                           False: diminuir brilho.
        Output: Salva imagem no diretório
    '''
    if len(img.shape) > 2:
      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    else:
      img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
      hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    if(option == True):
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        b = 'aumentou'
    elif(option == False):
        lim = 0 + value
        v[v<lim] = 0
        v[v>=lim] -= value
        b = 'diminuiu'

    final_hsv = cv2.merge((h, s, v))
    img2 = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    #cv2.imwrite("image_processed.jpg", img)
    viewImage(img2, 'Brilho %s em %d'%(b,value))
    return saveChanges(img, img2)


def subamostragem(image,amostra=2):
  if len(image.shape) > 2:
    image2=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #a imagem vem em formato BGR
    new_shape = (int((image2.shape[0] + 0.5)/amostra), int((image2.shape[1] + 0.5)/amostra), image2.shape[2]) #divide a imagem em 1/4
    img_sub = np.zeros((new_shape[0],new_shape[1],new_shape[2]), np.uint8)
    for x in range(new_shape[0]):
      for y in range(new_shape[1]):
        for z in range(new_shape[2]):
          img_sub[x][y][z] = image2[(x*amostra)][(y*amostra)][z]
    img_sub=cv2.cvtColor(img_sub,cv2.COLOR_RGB2BGR)

  else:
    new_shape = (int((image.shape[0] + 0.5)/amostra), int((image.shape[1] + 0.5)/amostra)) #divide a imagem em 1/4
    #print("new shape: ", new_shape)
    img_sub = np.zeros((new_shape[0],new_shape[1]), np.uint8)
    #print(img_bin.shape)
    for x in range(new_shape[0]):
      for y in range(new_shape[1]):
        img_sub[x][y] =  int(image[(x*amostra)][(y*amostra)])
  
  viewImage(img_sub,'Subamostragem em %d, dimensões: %dx%d'%(amostra, new_shape[0], new_shape[1]))
  return saveChanges(image, img_sub)


def binarizar(image, limiar=128):
  #Binarização da imagem
  if len(image.shape) > 2:
    image2 = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  else:
    image2 = image

  img_bin = np.zeros(image2.shape, np.uint8)
  
  #passa a dimensão y (sao invertidos), mas aqui usa-se o x por convencao
  for x in range(img_bin.shape[0]): 
    for y in range(img_bin.shape[1]):
      #print(img_gray[x][y])
      if image2[x][y] <= limiar:
        img_bin[x][y] = 0 #ausência de cor é preto (baixa cor)
      else:
        img_bin[x][y] = 255 #muita cor, branco

  viewImage(img_bin, 'Imagem binarizada em %d'%limiar)
  return saveChanges(image, img_bin)



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
                      Q: Sair

                      Imagens no sistema: %s

                      Opção: """ % str(names))

    if choice=="Q" or choice=="q":
        sys.exit

    elif choice == "A" or choice =="a":
      n = 1 - options(images, names, 'Qual das imagens deseja sobrescrever?')
      images[n], names[n] = loadImage()

    elif images[0] is None and images[1] is None:
      print('Nenhuma imagem no sistema')
      print('<Pressione ENTER para continuar>')
      input()
      
    elif choice == "B" or choice =="b":
      if images[1] is None:
        viewImage(images[0], names[0])
      elif images[0] is None:
        viewImage(images[1], names[1])
      else:
        viewImages(images, names)
      

    elif choice == "C" or choice =="c":
      n = options(images, names, 'Qual das imagens deseja salvar?')
      saveImage(images[n])

    elif choice=="D" or choice=="d":
      viewHistograms(images[0])
      viewHistograms(images[1])
      

    elif choice=="E" or choice=="e":
      option = 'A'
      if images[0] is None or images[1] is None:
        print('Sao necessarias duas imagens no sistema para calcular a diferenca')
        option = input('Deseja carregar outra imagem ? A:sim B:nao  :')

        if (option == 'A' or option == 'a') and images[0] is None:
          images[0], names[0] = loadImage()
        elif (option == 'A' or option == 'a') and images[1] is None:
          images[1], names[1] = loadImage()

      if (option == 'A' or option == 'a') and images[0] is not None and images[1] is not None:
        calImgDif(images[0], images[1])

    elif choice=="F" or choice=="f":
      n = options(images, names, 'Qual das imagens deseja alterar a intensidade?')
      
      value = 0
      print('(Utilize valor negativo para diminuir e positivo para aumentar)')
      value = input('A intensidade será alterada em quanto?  [-255,255] :')
      value = int(value)
      
      if value >= -255 and value <= 255:
        images[n] = itensidade(images[n], abs(value), (value>0))

    elif choice=="G" or choice=="g":
      n = options(images, names, 'Qual das imagens deseja alterar o brilho?')
      
      print('(Utilize valor negativo para diminuir e positivo para aumentar)')
      value = input('O brilho será alterado em quanto?  [-255,255] :')
      value = int(value)
      
      if value >= -255 and value <= 255:
        images[n] = brightness(images[n], abs(value), (value>0))

    elif choice=="H" or choice=="h":
      n = options(images, names, 'Qual das imagens deseja alterar a amostragem?')
      
      print(' O valor de amostragem, aqui, representa, aproximadamente, quantos pixels serão unidos em x e y.')
      print(' Este valor é aproximado porque as dimensoes da imagem podem não ser multiplas do valor da amostragem')
      value = input('A amostragem será alterado em quanto?  (0 < amostragem) :')
      value = int(value)

      if value > 0:
        images[n] = subamostragem(images[n], value)
    
    elif choice=='I' or choice=='i':
      n = options(images, names, 'Qual das imagens deseja binarizar?')

      value = input('Limiar?  (0 < limiar < 255) :')
      value = int(value)

      if value > 0 and value < 255:
        images[n] = binarizar(images[n], value)
    else:
      print("You must only select either A,B,C,D,E,F,G or Q.")
      print("Please try again")


if __name__=="__main__":
  from utils import options, saveChanges
  menu()