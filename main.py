import pygame
import time
import math
from utils import scale_image


# ARQUIVO PRINCIPAL


# Carregando as imagens (Capitalizadas por serem constantes)
GRASS = scale_image(pygame.image.load('imgs/grass.jpg'), 2.5)
TRACK = scale_image(pygame.image.load('imgs/track.png'), 0.8)

TRACK_BORDER = scale_image(pygame.image.load('imgs/track-border.png'), 0.8)
FINISH = pygame.image.load('imgs/finish.png')

RED_CAR = scale_image(pygame.image.load('imgs/red-car.png'), 0.55)
GREEN_CAR = scale_image(pygame.image.load('imgs/green-car.png'), 0.55)


# Criando a janela do jogo
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height() # Pegando o tamanho do circuito
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # Tornando a janela do tamanho do cirtuito
pygame.display.set_caption('FORMULA E SIMULATOR')


FPS = 60


# Função para renderizar as imagens
def render(window, images):
    for img, pos in images:
        window.blit(img, pos)


run = True # Mantém o jogo ativo
clock = pygame.time.Clock()
# Lista de imagens e suas posições de renderização
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]


# Game Loop
while run:
    clock.tick(FPS) # Faz com que o jogo mantenha 60 quadros for segundo

    render(WINDOW, images)
    pygame.display.update() # Atualiza a tela

    # Checa os eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Encerra o Game Loop ao fechar a janela
            run = False
            break

pygame.quit()