import pygame
import time
import math
from utils import scale_image, blit_rotate_center


# ARQUIVO PRINCIPAL


# Carregando as imagens
grass = scale_image(pygame.image.load('imgs/bg.png'), 7)
track = scale_image(pygame.image.load('imgs/track2.png'), 7)

track_border = scale_image(pygame.image.load('imgs/border2.png'), 7)
track_border_mask = pygame.mask.from_surface(track_border) # Máscara de colisão do circuito

finish = scale_image(pygame.image.load('imgs/finish2.png'), 7)
finish_mask = pygame.mask.from_surface(finish)
finish_position = (259, 350)

red_car = scale_image(pygame.image.load('imgs/racecar.png'), 1.7)
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
    
    # Função para reiniciar o carro na posição inicial
    def reset(self):
        self.x, self.y = self.start_pos
        self.angle = 0
        self.vel = 0


# Classe filha para o carro do player
class PlayerCar(AbstractCar):
    image = red_car
    start_pos = (288, 175)

    # Função para desacelerar o carro
    def reduce_speed(self):
        # Desacelera o carro pela metade da aceleração, até que a velocidade seja 0
        self.vel = max(self.vel - self.acceleration / 1.5, 0)
        self.move() # Continua movendo o carro ao desacelerar

    # Função para rebater o carro ao colidir
    def bounce(self):
        self.vel = -self.vel / 2 # Inverte a direção da velocidade
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
images = [(grass, (0, 0)), (track, (0, 0)), (finish, finish_position), (track_border, (0, 0))]
# Carro do jogador com velocidade máxima 5 e velocidade de rotação 5
player_car = PlayerCar(9, 5)
nickname = input('Digite seu nome: ')
print()
print(f'------- Piloto {nickname} -------')
timer = 0 # Tempo da volta
lap = 1 # Número da volta
laps = [] # Lista com timer de cada volta

# Game Loop
while run:
    timer += 1 # Acrecenta um no timer
    clock.tick(fps) # Faz com que o jogo mantenha 60 quadros for segundo

    render(window, images, player_car)

    # Verifica os eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Encerra o Game Loop ao fechar a janela
            run = False
            break

    move_player(player_car)

    # Verifica se o carro colidiu
    if player_car.collide(track_border_mask) != None:
        player_car.bounce()

    finish_poi_collide = player_car.collide(finish_mask, *finish_position)
    if finish_poi_collide != None: # * Divide em 2 argumentos (x e y)
        if finish_poi_collide[1] == 0: # Se o carro colidir com a parte de cima da linha de chegada
            player_car.bounce()
        else:
            player_car.reset()
            print(f'Volta {lap}: {(timer / 60) + 2:.2f}s')
            laps.append((timer / 60) + 2) # Adiciona o tempo da volta na lista
            timer = 0 # Redefine o tempo da volta para 0
            lap += 1 # Adiciona mais uma volta

best_lap = min(laps) # Determina o menor tempo
print()
print(f'- Melhor volta: {best_lap:.2f} segundos!')
pygame.quit() # Encerra o jogo