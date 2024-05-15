import pygame
import time
import math
from utils import scale_image, blit_rotate_center


# ARQUIVO PRINCIPAL


# Carregando as imagens
grass = scale_image(pygame.image.load('imgs/grass.jpg'), 2.5)
track = scale_image(pygame.image.load('imgs/track.png'), 0.8)

track_border = scale_image(pygame.image.load('imgs/track-border.png'), 0.8)
finish = pygame.image.load('imgs/finish.png')

red_car = scale_image(pygame.image.load('imgs/red-car.png'), 1.7)
green_car = scale_image(pygame.image.load('imgs/green-car.png'), 0.55)


# Criando a janela do jogo
width, height = track.get_width(), track.get_height() # Pegando o tamanho do circuito
window = pygame.display.set_mode((width, height)) # Tornando a janela do tamanho do cirtuito
pygame.display.set_caption('FORMULA E SIMULATOR')


# Classe pai dos carros
class AbstractCar:
    def __init__(self, max_vel, rotation_vel): # Método Construtor
        self.img = self.image
        self.max_vel = max_vel # Velocidade máxima
        self.vel = 0 # Velocidade
        self.rotation_vel = rotation_vel # Velocidade de rotação
        self.angle = 0 # Ângulo
        self.x, self.y = self.start_pos # Posição inicial

    def rotate(self, left=False, right=False): # Rotaciona o carro
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def render(self, window): # Renderiza o carro
        blit_rotate_center(window, self.img, (self.x, self.y), self.angle)


# Classe filha para o carro do player
class PlayerCar(AbstractCar):
    image = red_car
    start_pos = (160, 200)


# Função para renderizar as imagens
def render(window, images, player_car):
    for img, pos in images:
        window.blit(img, pos)

    player_car.render(window)
    pygame.display.update() # Atualiza a tela


fps = 60
run = True # Mantém o jogo ativo
clock = pygame.time.Clock()
# Lista de imagens e suas posições de renderização
images = [(grass, (0, 0)), (track, (0, 0))]
# Carro do jogador com velocidade 5 e velocidade de rotação 5
player_car = PlayerCar(5, 5)


# Game Loop
while run:
    clock.tick(fps) # Faz com que o jogo mantenha 60 quadros for segundo

    render(window, images, player_car)

    # Checa os eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Encerra o Game Loop ao fechar a janela
            run = False
            break

    keys = pygame.key.get_pressed() # Se uma tecla for pressionada

    # Se a tecla A for pressionada o carro rotaciona para a esquerda
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    # Se a tecla D for pressionada o carro rotaciona para a direita
    if keys[pygame.K_d]:
        player_car.rotate(right=True)


    
pygame.quit()