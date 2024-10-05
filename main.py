import pygame
import sys
import math
import json
import uuid
from utils import scale_image, blit_rotate_center

pygame.init()

# Constantes (Cores)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Função para carregar imagens
def load_images():
    images = {}
    images['background'] = scale_image(pygame.image.load('imgs/bg.png'), 7)
    images['track'] = scale_image(pygame.image.load('imgs/track2.png'), 7)
    images['track_border'] = scale_image(pygame.image.load('imgs/border.png'), 7)
    images['finish'] = scale_image(pygame.image.load('imgs/finish2.png'), 7)
    images['red_car'] = scale_image(pygame.image.load('imgs/bluecar.png'), 1.7)
    images['dash'] = scale_image(pygame.image.load('imgs/dash.png'), 7)
    images['life'] = [scale_image(pygame.image.load(f'imgs/bolt{i}.png'), 7) for i in range(1, 6)]
    images['tutorial'] = scale_image(pygame.image.load('imgs/tutorial.png'), 7)

    # Carregando as imagens da animação de início
    animation_frames = []
    for i in range(1, 15):
        frame_path = f'imgs/start_animation{i}.png'
        try:
            frame_image = scale_image(pygame.image.load(frame_path), 7)
            animation_frames.append(frame_image)
        except pygame.error as e:
            print(f'Erro ao carregar {frame_path}: {e}')
    images['start_animation'] = animation_frames

    # Carregando as imagens da animação de game over
    gameover_frames = []
    for i in range(1, 6):
        gameover_path = f'imgs/gameover{i}.png'
        try:
            gameover_image = scale_image(pygame.image.load(gameover_path), 7)
            gameover_frames.append(gameover_image)
        except pygame.error as e:
            print(f'Erro ao carregar {gameover_path}: {e}')
    images['gameover_animation'] = gameover_frames

    # Carregando as imagens da animação de SpeedPoints
    speedpoints_frames = []
    for i in range(1, 6):
        speedpoints_path = f'imgs/sp{i}.png'
        try:
            speedpoints_image = scale_image(pygame.image.load(speedpoints_path), 7)
            speedpoints_frames.append(speedpoints_image)
        except pygame.error as e:
            print(f'Erro ao carregar {speedpoints_path}: {e}')
    images['speedpoints_animation'] = speedpoints_frames

    return images


class Game:
    def __init__(self):
        self.images = load_images()
        self.setup_display()  # Define self.width e self.height

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'START'
        self.player_name = ''
        self.player_car = PlayerCar(self.images['red_car'], (288, 175))
        self.lives = 5
        self.laps = []
        self.dash_active = False
        self.dash_timer = 0
        self.dash_duration = 50
        self.finish_position = (259, 350)  # Posição de chegada
        self.timer = 0
        self.lap = 1
        self.max_laps = 2
        self.current_life_image = self.images['life'][0]
        self.speedpoints_earned = 0  # Inicializa com 0
        self.init_music()
        self.fonts = {
            'title': pygame.font.Font('fonts/PixelifySans-Bold.ttf', 120),
            'common': pygame.font.Font('fonts/PixelifySans-Medium.ttf', 65)
        }

        self.data_saved = False
        
        # Reintegrando as máscaras de colisão
        self.track_border_mask = pygame.mask.from_surface(self.images['track_border'])
        self.finish_mask = pygame.mask.from_surface(self.images['finish'])
        self.dash_mask = pygame.mask.from_surface(self.images['dash'])

        # Variáveis da animação da tela inicial
        self.animation_frames = self.images['start_animation']
        self.current_animation_frame = 0
        self.animation_speed = 5  # Número de frames do jogo por mudança de frame da animação
        self.animation_counter = 0

        # Variáveis de animação de game over
        self.gameover_frames = self.images['gameover_animation']
        self.current_gameover_frame = 0
        self.gameover_speed = 7  # Número de frames do jogo por mudança de frame da animação de game over
        self.gameover_counter = 0

        # Variáveis de animação de speedpoints
        self.speedpoints_frames = self.images['speedpoints_animation']
        self.speedpoints_to_show = []  # Lista de frames a serem exibidos
        self.current_speedpoints_frame = 0
        self.speedpoints_speed =10  # Número de frames do jogo por mudança de frame da animação de game over
        self.speedpoints_counter = 0
        self.speedpoints_wait_timer = 0  # Contador para aguardar 3 segundos após a animação
        self.speedpoints_display_duration = 180  # 3 segundos a 60 FPS

        # Variáveis para o tutorial
        self.tutorial_start_time = None
        self.tutorial_duration = 4000  # Duração total do tutorial em milissegundos (7 segundos)
        self.tutorial_fade_in_duration = 1000  # Duração do fade-in em milissegundos (2 segundos)
        self.tutorial_full_opacity_duration = 2000  # Duração em opacidade total (3 segundos)
        self.tutorial_fade_out_duration = 1000  # Duração do fade-out em milissegundos (2 segundos)

        # Superfície preta para fade-in e fade-out
        self.fade_surface = pygame.Surface((self.width, self.height))
        self.fade_surface.fill(BLACK)
        self.fade_alpha = 255  # Inicia totalmente opaco para o fade-in
        self.fade_surface.set_alpha(self.fade_alpha)


    def init_music(self):
        try:
            pygame.mixer.music.load('sound/soundtrack.mp3')
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erro ao carregar soundtrack.mp3: {e}")

    def setup_display(self):
        self.width, self.height = self.images['track'].get_width(), self.images['track'].get_height()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('FORMULA E SIMULATOR')

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update_game_logic()
            self.render()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.state == 'START':
                    if event.key == pygame.K_i:
                        self.state = 'GET_NAME'
                    elif event.key == pygame.K_s:
                        self.running = False

                elif self.state == 'GET_NAME':
                    if event.key == pygame.K_RETURN and self.player_name.strip():
                        self.state = 'TUTORIAL'
                        self.tutorial_start_time = pygame.time.get_ticks()
                        self.fade_alpha = 255  # Inicia totalmente opaco para o fade-in
                        self.fade_surface.set_alpha(self.fade_alpha)
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        self.player_name += event.unicode

                elif self.state in ['GAME_OVER', 'FINISHED']:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_r and self.state in ['GAME_OVER', 'FINISHED']:
                        self.reset_game()

    def reset_game(self):
        self.player_car.reset()
        self.lives = 5
        self.current_life_image = self.images['life'][0]
        self.laps = []
        self.timer = 0
        self.lap = 1
        self.state = 'PLAYING'
        self.dash_active = False
        self.dash_timer = 0
        self.player_car.max_vel = 11
        self.player_car.acceleration = 0.2
        self.data_saved = False  # Resetar a flag para permitir salvar novamente

    def update_game_logic(self):
        if self.state == 'PLAYING':
            self.timer += 1
            self.player_car.update(pygame.key.get_pressed())

            if self.dash_active:
                self.dash_timer += 1
                if self.dash_timer >= self.dash_duration:
                    self.dash_active = False
                    self.player_car.max_vel = 11
                    self.player_car.acceleration = 0.2

            if not self.dash_active and self.player_car.collide(self.dash_mask, 0, 0):
                self.dash_active = True
                self.dash_timer = 0
                self.player_car.acceleration = 2
                self.player_car.max_vel = 17

            if self.player_car.collide(self.track_border_mask, 0, 0):
                self.player_car.bounce()
                self.lives -= 1
                if self.lives >= 1:
                    self.current_life_image = self.images['life'][5 - self.lives]
                else:
                    self.state = 'GAME_OVER'

            finish_poi_collide = self.player_car.collide(self.finish_mask, *self.finish_position)
            if finish_poi_collide:
                if finish_poi_collide[1] == 0:
                    self.player_car.bounce()
                else:
                    self.player_car.reset()
                    self.laps.append((self.timer / 60) + 2)
                    self.timer = 0
                    self.lap += 1
                    if self.lap > self.max_laps:
                        self.save_player_data() # Salva os dados ao completar as voltas
                        self.setup_speedpoints_animation()
                        self.state = 'SPEEDPOINTS'

        elif self.state == 'START':
            # Atualizar a animação da tela inicial
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.current_animation_frame += 1
                if self.current_animation_frame >= len(self.animation_frames):
                    self.current_animation_frame = 0  # Reinicia a animação (loop)

        elif self.state == 'SPEEDPOINTS':
            if self.current_speedpoints_frame < len(self.speedpoints_to_show):
                self.speedpoints_counter += 1
                if self.speedpoints_counter >= self.speedpoints_speed:
                    self.speedpoints_counter = 0
                    self.current_speedpoints_frame += 1
            else:
                # Inicia o contador de espera de 3 segundos após a animação
                self.speedpoints_wait_timer += 1
                if self.speedpoints_wait_timer >= self.speedpoints_display_duration:
                    self.state = 'FINISHED'  # Muda para a tela de Finished

        elif self.state == 'GAME_OVER':
            # Atualizar a animação de game over
            self.gameover_counter += 1
            if self.gameover_counter >= self.gameover_speed:
                self.gameover_counter = 0
                self.current_gameover_frame += 1
                if self.current_gameover_frame >= len(self.gameover_frames):
                    self.current_gameover_frame = 0  # Reinicia a animação (loop)

        elif self.state == 'TUTORIAL':
            # Lógica para o efeito de fade-in e fade-out
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.tutorial_start_time

            if elapsed_time <= self.tutorial_fade_in_duration:
                # Fade-in: diminui a opacidade da superfície preta de 255 para 0
                fade_progress = elapsed_time / self.tutorial_fade_in_duration
                self.fade_alpha = int(255 * (1 - fade_progress))
                self.fade_surface.set_alpha(self.fade_alpha)
            elif elapsed_time <= self.tutorial_fade_in_duration + self.tutorial_full_opacity_duration:
                # Opacidade total: mantém a superfície preta totalmente transparente
                self.fade_alpha = 0
                self.fade_surface.set_alpha(self.fade_alpha)
            elif elapsed_time <= self.tutorial_duration:
                # Fade-out: aumenta a opacidade da superfície preta de 0 para 255
                fade_out_elapsed = elapsed_time - (self.tutorial_fade_in_duration + self.tutorial_full_opacity_duration)
                fade_progress = fade_out_elapsed / self.tutorial_fade_out_duration
                fade_progress = min(fade_progress, 1)  # Garante que não ultrapasse 1
                self.fade_alpha = int(255 * fade_progress)
                self.fade_surface.set_alpha(self.fade_alpha)
            else:
                # Fim do tutorial, iniciar o jogo
                self.state = 'PLAYING'

    def render(self):
        if self.state == 'START':
            self.window.blit(self.animation_frames[self.current_animation_frame], (0, 0))

        elif self.state == 'GET_NAME':
            self.window.fill(BLACK)
            self.render_text("Digite seu nome:", 'title', WHITE, -100)
            name_surface = self.fonts['common'].render(self.player_name, True, WHITE)
            name_rect = name_surface.get_rect(center=(self.width / 2, self.height / 2))
            self.window.blit(name_surface, name_rect)

        elif self.state == 'TUTORIAL':
            # Renderizar a imagem do tutorial
            if self.images['tutorial']:
                self.window.blit(self.images['tutorial'], (0, 0))
                # Renderizar a superfície preta para o fade-in e fade-out
                self.window.blit(self.fade_surface, (0, 0))
            else:
                self.window.fill(BLACK)
                self.render_text("Tutorial não encontrado.", 'common', WHITE, 0)

        elif self.state == 'PLAYING':
            self.window.blit(self.images['background'], (0, 0))
            self.window.blit(self.images['track'], (0, 0))
            self.window.blit(self.images['finish'], self.finish_position)
            self.window.blit(self.images['dash'], (0, 0))
            self.window.blit(self.images['track_border'], (0, 0))
            self.player_car.render(self.window)
            self.window.blit(self.current_life_image, (10, 10))

            if self.dash_active:
                overlay = pygame.Surface((self.width, self.height))
                overlay.set_alpha(20)
                overlay.fill((255, 28, 174))  # Cor do overlay (rosa forte)
                self.window.blit(overlay, (0, 0))

        elif self.state == 'GAME_OVER':
            if self.gameover_frames:
                self.window.blit(self.gameover_frames[self.current_gameover_frame], (0, 0))

        elif self.state == 'SPEEDPOINTS':
            if self.current_speedpoints_frame < len(self.speedpoints_to_show):
                current_frame_image = self.speedpoints_to_show[self.current_speedpoints_frame]
                frame_rect = current_frame_image.get_rect(center=(self.width / 2, self.height / 2))
                self.window.blit(current_frame_image, frame_rect)

        elif self.state == 'FINISHED':
            self.window.fill(BLACK)
            self.render_info(self.player_name, self.laps, self.fonts['common'])

        pygame.display.update()

    def render_text(self, text, font_name, color, y_offset):
        text_surface = self.fonts[font_name].render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2 + y_offset))
        self.window.blit(text_surface, text_rect)

    def render_info(self, player_name, laps, font):
        self.render_text(f'Piloto: {player_name}', 'common', WHITE, -300)
        if laps:
            for i, lap_time in enumerate(laps, start=1):
                self.render_text(f'Volta {i}: {lap_time:.2f}s', 'common', WHITE, (-70 * i))
            best_lap = min(laps)
            self.render_text(f'Melhor Volta: {best_lap:.2f}s', 'common', WHITE, (70 * (len(laps) + 1)))

    def calculate_speedpoints(self, total_time):
        """
            Calcula os speedpoints com base no tempo total da corrida.
        """
        if total_time <= 16:
            return 500
        elif total_time <= 19:
            return 300
        elif total_time <= 22:
            return 150
        elif total_time <= 25:
            return 50
        else:
            return 10

    def setup_speedpoints_animation(self):
        if self.speedpoints_earned >= 500:
            self.speedpoints_to_show = self.speedpoints_frames[:5]
        elif self.speedpoints_earned >= 300:
            self.speedpoints_to_show = self.speedpoints_frames[:4]
        elif self.speedpoints_earned >= 150:
            self.speedpoints_to_show = self.speedpoints_frames[:3]
        elif self.speedpoints_earned >= 50:
            self.speedpoints_to_show = self.speedpoints_frames[:2]
        else:
            self.speedpoints_to_show = self.speedpoints_frames[:1]

        self.current_speedpoints_frame = 0
        self.speedpoints_counter = 0
        self.speedpoints_wait_timer = 0

    def save_player_data(self):
        if not self.data_saved:
            # Dados da corrida atual
            total_time = round(sum(self.laps), 2) if self.laps else 0
            speedpoints_earned = self.calculate_speedpoints(total_time)

            race_data = {
                'laps': [round(lap, 2) for lap in self.laps], # Formata os tempos das voltas
                'best_lap': round(min(self.laps), 2) if self.laps else None,
                'total_time': total_time,
                'speedpoints': self.calculate_speedpoints(total_time)
            }

            try:
                # Tenta abrir o arquivo existente para carregar os dados
                with open('players_data.json', 'r', encoding='utf-8') as archive:
                    data = json.load(archive)
            except (FileNotFoundError, json.JSONDecodeError):
                # Se o arquivo não existir, inicia uma lista vazia
                data = {}


            # Verifica se o jogador já está registrado
            player_id = None
            for pid, player in data.items():
                if player['player_name'].lower() == self.player_name.lower():
                    player_id = pid
                    break # Interrompe a busca pelo jogador

            if player_id != None:
                # Adiciona a corrida à lista de corridas do jogador existente
                data[player_id]['races'].append(race_data)
                # Atualiza os speedpoints totais
                data[player_id]['total_speedpoints'] += race_data['speedpoints']
                print(f'Corrida adicionada ao ID de jogador: {player_id}.')
            else:
                # Gera um novo ID único para o jogador
                player_id = str(uuid.uuid4())
                # Adiciona ao ID, o nome e a corrida atual do jogador
                data[player_id] = {
                    'player_name': self.player_name,
                    'total_speedpoints': race_data['speedpoints'], # Inicializa com os speedpoints da primeira corrida
                    'races': [race_data]
                }
                print(f'Novo jogador registrado com ID: {player_id}.')

            try:
                # Salva os dados atualizados de volta no arquivo json
                with open('players_data.json', 'w', encoding='utf-8') as archive:
                    json.dump(data, archive, ensure_ascii=False, indent=4)
                print('Dados do jogador salvos com sucesso!')

                # Armazena os SpeedPoints ganhos para a animação
                self.speedpoints_earned = speedpoints_earned

                self.data_saved = True
            except Exception as e:
                print(f'Erro ao salvar dados do jogador: {e}')


class PlayerCar:
    def __init__(self, image, start_pos):
        self.image = image
        self.start_pos = start_pos
        self.x, self.y = self.start_pos
        self.angle = 0
        self.vel = 0
        self.max_vel = 11
        self.rotation_vel = 7
        self.acceleration = 0.2

    def reset(self):
        self.x, self.y = self.start_pos
        self.angle = 0
        self.vel = 0

    def update(self, keys):
        self.move(keys)
        self.move_car()

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rotate(left=True)
        if keys[pygame.K_d]:
            self.rotate(right=True)
        if keys[pygame.K_w]:
            self.move_forward()
        elif keys[pygame.K_s]:
            self.move_backward()
        else:
            self.reduce_speed()

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 1.5, 0)

    def move_car(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal

    def bounce(self):
        self.vel = -self.vel / 2
        self.move_car()

    def render(self, window):
        blit_rotate_center(window, self.image, (self.x, self.y), self.angle)

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

if __name__ == '__main__':
    game = Game()
    game.run()
