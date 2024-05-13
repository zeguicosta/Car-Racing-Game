import pygame
import time
import math

# Carregando as imagens (Capitalizadas por serem constantes)
GRASS = pygame.image.load('imgs/grass.jpg')
TRACK = pygame.image.load('imgs/track.png')

TRACK_BORDER = pygame.image.load('imgs/track-border.png')
FINISH = pygame.image.load('imgs/finish.png')

RED_CAR = pygame.image.load('imgs/red-car.png')
GREEN_CAR = pygame.image.load('imgs/green-car.png')


# Criando a janela do jogo
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height() # Pegando o tamanho do circuito
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # Tornando a janela do tamanho do cirtuito
pygame.display.set_caption('FORMULA E SIMULATOR')