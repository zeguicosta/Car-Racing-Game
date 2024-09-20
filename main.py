import pygame
import sys
import time
import math
from utils import scale_image, blit_rotate_center

pygame.init()

# Carregando as imagens
background = scale_image(pygame.image.load('imgs/bg.png'), 7)
track = scale_image(pygame.image.load('imgs/track2.png'), 7)
track_border = scale_image(pygame.image.load('imgs/border.png'), 7)
track_border_mask = pygame.mask.from_surface(track_border) # Máscara de colisão do circuito
finish = scale_image(pygame.image.load('imgs/finish2.png'), 7)
finish_mask = pygame.mask.from_surface(finish)
finish_position = (259, 350)
red_car = scale_image(pygame.image.load('imgs/bluecar.png'), 1.7)
green_car = scale_image(pygame.image.load('imgs/green-car.png'), 0.55)
init_screen = scale_image(pygame.image.load('imgs/start_screen.png'), 7)
game_over = scale_image(pygame.image.load('imgs/gameover.png'), 7)
dash = scale_image(pygame.image.load('imgs/dash.png'), 7)
dash_mask = pygame.mask.from_surface(dash) # Máscara de colisão do dash

# Cores
white = (255, 255, 255)
black = (0, 0, 0)

# Fontes
title_font = pygame.font.Font('fonts/PixelifySans-Bold.ttf', 120)
commom_font = pygame.font.Font('fonts/PixelifySans-Medium.ttf', 65)

# Música
pygame.mixer.music.load('sound/soundtrack.mp3')
pygame.mixer.music.play(-1) # Executa a música infinitamente

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
        self.acceleration = 0.2 # Aceleração

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









# Tela Inicial

# Função que renderiza o texto
def render_text(surface, text, font, color, y_offset):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center = (width/2, height/2 + y_offset))
    surface.blit(text_surface, text_rect)


# Função que renderiza a tela inicial
def start_screen():
    while True:
        window.blit(init_screen, (0, 0))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    return
                if event.key == pygame.K_s:
                    pygame.quit()
                    sys.exit()


# Função para obter o nome do jogador
def get_player_name():
    player_name = ""
    active = True

    while active:
        window.fill(black)
        
        render_text(window, "Digite seu nome:", title_font, white, -100)
        name_surface = commom_font.render(player_name, True, white)
        name_rect = name_surface.get_rect(center = (width / 2, height / 2))
        window.blit(name_surface, name_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Remove o último caractere
                else:
                    player_name += event.unicode  # Adiciona o caractere digitado

    return player_name







# Tela final

# Função que exibe as informações da volta
def render_info(surface, player_name, laps, font):
    render_text(surface, f'Piloto: {player_name}', font, white, -300)
    if laps:
        for i, lap_time in enumerate(laps, start=1):
            render_text(surface, f'Volta {i}: {lap_time:.2f}s', font, white, (-70 * i))
    
    best_lap = min(laps)
    render_text(surface, f'Melhor Volta: {best_lap:.2f}s', font, white, (70 * (len(laps) + 1)))
    







# Jogo

# Função que faz o jogo rodar
def main(player_name):
    fps = 60
    run = True # Mantém o jogo ativo
    clock = pygame.time.Clock()
    # Lista de imagens e suas posições de renderização
    images = [(background, (0, 0)), (track, (0, 0)), (finish, finish_position), (track_border, (0, 0)), (dash, (0, 0))]
    # Carro do jogador com velocidade máxima 5 e velocidade de rotação 5
    player_car = PlayerCar(11, 7)
    print(f'------- Piloto {player_name} -------')
    lives = 5
    timer = 0 # Tempo da volta
    lap = 1 # Número da volta
    laps = [] # Lista com timer de cada volta
    dash_active = False
    dash_timer = 0
    dash_duration = 60 # Duração do dash (1 segundo, considerando 60 fps)

    full_life = scale_image(pygame.image.load('imgs/bolt.png'), 7)
    current_life = full_life

    # Game Loop
    while run:
        timer += 1 # Acrecenta um no timer
        clock.tick(fps) # Faz com que o jogo mantenha 60 quadros for segundo

        render(window, images, player_car)
        window.blit(current_life, (0, 0))

        # Verifica se o efeito do dash está ativo e controla o tempo
        if dash_active:
            dash_timer += 1
            overlay = pygame.Surface((width, height))  # Cria uma superfície do tamanho da tela
            overlay.set_alpha(20)  # Define a transparência (0 a 255)
            overlay.fill((255, 28, 174))  # Preenche a superfície com a cor azul
            window.blit(overlay, (0, 0))  # Desenha a superfície azul por cima da tela
            if dash_timer >= dash_duration:
                dash_active = False
                player_car.max_vel = 11  # Retorna a velocidade original
                player_car.acceleration = 0.2 # Retorna a aceleração original

        # Verifica os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Encerra o Game Loop ao fechar a janela
                run = False
                break

        move_player(player_car)

        if not dash_active and player_car.collide(dash_mask) != None:
            dash_active = True
            dash_timer = 0
            player_car.acceleration = 1
            player_car.max_vel = 15
        

        # Verifica se o carro colidiu
        if player_car.collide(track_border_mask) != None:
            player_car.bounce()
            lives -= 1

        match lives:
            case 4:
                current_life = scale_image(pygame.image.load('imgs/bolt2.png'), 7)
            case 3:
                current_life = scale_image(pygame.image.load('imgs/bolt3.png'), 7)
            case 2:
                current_life = scale_image(pygame.image.load('imgs/bolt4.png'), 7)
            case 1:
                current_life = scale_image(pygame.image.load('imgs/bolt5.png'), 7)
            case 0:
                run = False

        finish_poi_collide = player_car.collide(finish_mask, *finish_position)
        if finish_poi_collide != None: # * Divide em 2 argumentos (x e y)
            if finish_poi_collide[1] == 0: # Se o carro colidir com a parte de cima da linha de chegada
                player_car.bounce()
            else:
                player_car.reset()
                laps.append((timer / 60) + 2) # Adiciona o tempo da volta na lista
                timer = 0 # Redefine o tempo da volta para 0
                lap += 1 # Adiciona mais uma volta

            if lap > 2:  # Se o jogador completar 3 voltas
                        run = False  # Interrompe o jogo

        pygame.display.update()

    if lap > 2:
        # Exibe as informações na tela após o jogo ser interrompido
        window.fill(black)
        render_info(window, player_name, laps, commom_font)
        pygame.display.update()
    else:
        window.fill(black)
        window.blit(game_over, (0, 0))
        pygame.display.update()

     # Espera até o jogador fechar a janela
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    start_screen()
    main(get_player_name())