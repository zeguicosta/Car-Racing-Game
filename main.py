import pygame
import time
import math
from utils import scale_image, blit_rotate_center


# ARQUIVO PRINCIPAL


# Carregando as imagens
grass = scale_image(pygame.image.load('imgs/grass.jpg'), 2.5)
track = scale_image(pygame.image.load('imgs/track.png'), 0.8)

track_border = scale_image(pygame.image.load('imgs/track-border.png'), 0.8)
track_border_mask = pygame.mask.from_surface(track_border) # Máscara de colisão do circuito
finish = pygame.image.load('imgs/finish.png')

red_car = scale_image(pygame.image.load('imgs/red-car.png'), 1.5)
green_car = scale_image(pygame.image.load('imgs/green-car.png'), 0.55)


# Criando a janela do jogo
width, height = track.get_width(), track.get_height() # Pegando o tamanho do circuito
window = pygame.display.set_mode((width, height)) # Tornando a janela do tamanho do cirtuito
pygame.display.set_caption('FORMULA E SIMULATOR') # Título do jogo


# Classe pai dos carros
class AbstractCar:
    def __init__(self, max_vel, rotation_vel): # Método Construtor
        self.img = self.image
        self.max_vel = max_vel
        self.vel = 0 # Velocidade
        self.rotation_vel = rotation_vel # Velocidade de rotação
        self.angle = 0 # Ângulo
        self.x, self.y = self.start_pos
        self.acceleration = 0.15 # Aceleração

    def rotate(self, left=False, right=False): # Rotaciona o carro
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def render(self, window): # Renderiza o carro
        blit_rotate_center(window, self.img, (self.x, self.y), self.angle)

    # Função para aumentar a velocidade
    def move_forward(self):
        # Se (velocidade atual + aceleração) for menor que a velocidade máxima,
        # então essa será a velocidade do carro. Caso contrário, a velocidade máxima
        # será a velocidade do carro.
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move() # Move o carro

    # Função para dar ré
    def move_backward(self):
        # Diminui a velocidade pela a aceleração, até que a velocidade fique negativa
        # e seja igual a metade da velocidade máxima positiva.
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move() # Move o carro com a velocidade negativa

    # Função para mover o carro
    def move(self):
        radians = math.radians(self.angle) # Converte o ângulo em graus para radianos
        # Vy = cos(a) * V, Vx = sin(a) * V. (Na matemática seria invertido seno e cosseno,
        # entretanto, em jogos o ângulo inicial aponta para cima e não para a direita).
        vertical = math.cos(radians) * self.vel # Distância que o carro move em Y
        horizontal = math.sin(radians) * self.vel # Distância que o carro move em X

        self.y -= vertical # Move o carro verticalmente
        self.x -= horizontal # Move o carro horizontalmente

    # Função para colisão
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img) # Máscara de colisão do carro
        offset = (int(self.x - x), int(self.y - y))
        # Ponto de interseção
        poi = mask.overlap(car_mask, offset)
        return poi


# Classe filha para o carro do player
class PlayerCar(AbstractCar):
    image = red_car
    start_pos = (160, 200)

    # Função para desacelerar o carro
    def reduce_speed(self):
        # Desacelera o carro pela metade da aceleração, até que a velocidade seja 0
        self.vel = max(self.vel - self.acceleration / 1.5, 0)
        self.move() # Continua movendo o carro ao desacelerar

    # Função para rebater o carro ao colidir
    def bounce(self):
        self.vel = -self.vel # Inverte a direção da velocidade
        self.move() # Move o carro assim que inverte a velocidade


# Função para renderizar as imagens
def render(window, images, player_car):
    for img, pos in images:
        window.blit(img, pos)

    player_car.render(window)
    pygame.display.update() # Atualiza a tela

# Função para mover o carro do player
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    # Se a tecla A for pressionada o carro rotaciona para a esquerda
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    # Se a tecla D for pressionada o carro rotaciona para a direita
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    # Se a tecla W for pressionada o carro move para frente
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    # Se a tecla S for pressionada o carro move para trás
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    # Se o carro não estiver sendo movido pelo player, reduz a velocidade
    if not moved:
        player_car.reduce_speed()


fps = 60
run = True # Mantém o jogo ativo
clock = pygame.time.Clock()
# Lista de imagens e suas posições de renderização
images = [(grass, (0, 0)), (track, (0, 0))]
# Carro do jogador com velocidade máxima 5 e velocidade de rotação 5
player_car = PlayerCar(4, 5)


# Game Loop
while run:
    clock.tick(fps) # Faz com que o jogo mantenha 60 quadros for segundo

    render(window, images, player_car)

    # Verifica os eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Encerra o Game Loop ao fechar a janela
            run = False
            break

    move_player(player_car)

    # Verifica se o carro colidiu
    if player_car.collide(track_border_mask):
        player_car.bounce()
    
pygame.quit()