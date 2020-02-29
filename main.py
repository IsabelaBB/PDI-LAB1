import cv2
import numpy as np
import sys
import os
from matplotlib import pyplot as plt
from skimage.measure import compare_ssim

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
    #print(str(os.path.exists(filename)))
    #print(str(os.path.isfile(filename)))
    input()
    return None, ''
  image = cv2.imread(filename)
  if image is not None:
    return image, filename.split('/')[-1]
  print('ERRO: Ocorreu um erro ao abrir a imagem')
  input()
  return None,''


# - Visualizar arquivos de imagem acromáticas e de imagens coloridas 
def viewImage(image):
  #h, w, c = image.shape
  if image.shape[2] > 1:
    # imagem é colorida
    plt.imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
  else:
    # imagem está em escala de cinza
    plt.imshow(image, cmap='gray')
  plt.show()
  

# - Salvar arquivos de imagem acromáticas e de imagens coloridas em padrões específicos (jpg, bmp e png) 
def saveImage(image):
  print()
  filename = input('Digite o diretorio/arquivo onde quer salvar: ')
  cv2.imwrite(filename,image)


# - Calcular e visualizar o(s) histograma(s) de imagem acromáticas e de imagens coloridas 
# (opção de visualizar a imagem à esquerda, o histograma à direita) 
# - A partir de arquivos de imagens coloridas, separar as componentes R, G e B, para posterior processamento 
def viewHistograms(image1, image2):
  # se as imagens já forem cinza, a conversão gera um erro
  if image1 is not None:
    # imagem cinza
    if image1.shape[2] == 1:
      GR = cv2.calcHist([image1],[0],None,[256],[0,255])

      plt.subplot(121), plt.imshow(image1, cmap='gray', vmin=0, vmax=255)
      plt.subplot(122), plt.plot(GR, color='gray')

      plt.xlim([0,255])
      plt.show()

    # imagem colorida
    else:
      image1 = cv2.cvtColor(image1,cv2.COLOR_BGR2RGB)
      gray = cv2.cvtColor(image1,cv2.COLOR_RGB2GRAY)

      R = cv2.calcHist([image1],[0],None,[256],[0,255])
      G = cv2.calcHist([image1],[1],None,[256],[0,255])
      B = cv2.calcHist([image1],[2],None,[256],[0,255])
      GR = cv2.calcHist([gray],[0],None,[256],[0,255])

      plt.subplot(421), plt.imshow(image1[:,:,0], cmap='gray', vmin=0, vmax=255)
      plt.subplot(422), plt.plot(R,color='red')
      plt.subplot(423), plt.imshow(image1[:,:,1], cmap='gray', vmin=0, vmax=255)
      plt.subplot(424), plt.plot(G,color='green')
      plt.subplot(425), plt.imshow(image1[:,:,2], cmap='gray', vmin=0, vmax=255)
      plt.subplot(426), plt.plot(B,color='blue')
      plt.subplot(427), plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
      plt.subplot(428), plt.plot(GR, color='gray')

      plt.xlim([0,255])
      plt.show()

  if image2 is not None:
    # imagem cinza
    if image2.shape[2] == 1:
      GR = cv2.calcHist([image2],[0],None,[256],[0,255])

      plt.subplot(121), plt.imshow(image2, cmap='gray', vmin=0, vmax=255)
      plt.subplot(122), plt.plot(GR, color='gray')

      plt.xlim([0,255])
      plt.show()

    # imagem colorida
    else:
      image2 = cv2.cvtColor(image2,cv2.COLOR_BGR2RGB)
      gray = cv2.cvtColor(image2,cv2.COLOR_RGB2GRAY)

      R = cv2.calcHist([image2],[0],None,[256],[0,255])
      G = cv2.calcHist([image2],[1],None,[256],[0,255])
      B = cv2.calcHist([image2],[2],None,[256],[0,255])
      GR = cv2.calcHist([gray],[0],None,[256],[0,255])

      plt.subplot(421), plt.imshow(image2[:,:,0], cmap='gray', vmin=0, vmax=255)
      plt.subplot(422), plt.plot(R,color='red')
      plt.subplot(423), plt.imshow(image2[:,:,1], cmap='gray', vmin=0, vmax=255)
      plt.subplot(424), plt.plot(G,color='green')
      plt.subplot(425), plt.imshow(image2[:,:,2], cmap='gray', vmin=0, vmax=255)
      plt.subplot(426), plt.plot(B,color='blue')
      plt.subplot(427), plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
      plt.subplot(428), plt.plot(GR, color='gray')

      plt.xlim([0,255])
      plt.show()

    '''
    plt.subplot(411), plt.hist(image[:,:,0].ravel(),range=[0,255])
    plt.subplot(412), plt.hist(image[:,:,1].ravel(),range=[0,255])
    plt.subplot(413), plt.hist(image[:,:,2].ravel(),range=[0,255])
    plt.subplot(414), plt.plot(R,color='red'), plt.plot(G,color='green'), plt.plot(B,color='blue'), plt.plot(gray,color='gray')
    plt.xlim([0,256])
    plt.show()
    '''


# - Calcular a imagem-diferença entre duas imagens acromáticas 
# - Calcular as métricas ERRO MÉDIO QUADRÁTICO e PSNR a partir da imagem-diferença.
def calImgDif(image1, image2):
  # se as imagens já forem cinza, a conversão gera um erro
  if image1.shape[2] > 1:
    image1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)

  if image2.shape[2] > 1:
    image2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)

  # imagens com tamanhos diferentes precisam ser redimensionadas para o mesmo tamanho, ou também irá gerar erro
  if image1.size > image2.size:
    image1 = cv2.resize(image1,image2.shape[:2])
  elif image1.size < image2.size:
    image2 = cv2.resize(image2,image1.shape[:2])

  (score, diff) = compare_ssim(image1, image2, full=True)
  diff = (diff * 255).astype("uint8")
  plt.imshow(diff, cmap='gray')
  plt.title('Erro médio quadrático: '+str(np.square(diff).mean())+', PSNR: '+str(cv2.PSNR(image1, image2)))
  plt.show()


def menu():
  choice = ''
  image1 = None
  image2 = None
  name1 = ''
  name2 = ''

  while(choice is not 'Q' and choice is not 'q'):
    print("************MENU**************")
    #time.sleep(1)
    print()
    choice = input("""
                      A: Load image
                      B: Show image
                      C: Save image
                      D: Show Histograms
                      E: Compare with other image
                      Q: Quit

                      Please enter your choice: """)

    if choice=="Q" or choice=="q":
        sys.exit

    elif choice == "A" or choice =="a":
      option = ''
      if image1 is not None and image2 is not None:
        option = input('Qual das imagens deseja sobrescrever? A:'+name1+' B:'+name2+' :')
      if image1 is None or option == 'A' or option == 'a':
        image1, name1 = loadImage()
      elif image2 is None or option == 'B' or option == 'b':
        image2, name2 = loadImage()

    elif image1 is None and image2 is None:
      print('Nenhuma imagem no sistema')
      #input()
      
    elif choice == "B" or choice =="b":
      option = ''
      if image1 is not None and image2 is not None:
        option = input('Qual das imagens deseja visualizar? A:'+name1+' B:'+name2+' :')
      if image2 is None or option == 'A' or option == 'a':
        viewImage(image1)
      elif image1 is None or option == 'B' or option == 'b':
        viewImage(image2)
      

    elif choice == "C" or choice =="c":
      option = ''
      if image1 is not None and image2 is not None:
        option = input('Qual das imagens deseja salvar? A:'+name1+' B:'+name2+' :')
      if image2 is None or option == 'A' or option == 'a':
        saveImage(image1)
      elif image1 is None or option == 'B' or option == 'b':
        saveImage(image2)
        

    elif choice=="D" or choice=="d":
      viewHistograms(image1, image2)
      

    elif choice=="E" or choice=="e":
      option = 'A'
      if image1 is None or image2 is None:
        print('Sao necessarias duas imagens no sistema para calcular a diferenca')
        option = input('Deseja carregar outra imagem ? A:sim B:nao  :')

        if (option == 'A' or option == 'a') and image1 is None:
          image1, name1 = loadImage()
        elif (option == 'A' or option == 'a') and image2 is None:
          image2, name2 = loadImage()

      if (option == 'A' or option == 'a') and image1 is not None and image2 is not None:
        calImgDif(image1, image2)

    else:
      print("You must only select either A,B,C,D,E or Q.")
      print("Please try again")


if __name__=="__main__":
  menu()