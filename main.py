import pygame
import sys
import math
from utils import scale_image, blit_rotate_center

pygame.init()

# Constantes
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
    images['init_screen'] = scale_image(pygame.image.load('imgs/start_screen.png'), 7)
    images['game_over'] = scale_image(pygame.image.load('imgs/gameover.png'), 7)
    images['dash'] = scale_image(pygame.image.load('imgs/dash.png'), 7)
    images['life'] = [
        scale_image(pygame.image.load('imgs/bolt1.png'), 7),
        scale_image(pygame.image.load('imgs/bolt2.png'), 7),
        scale_image(pygame.image.load('imgs/bolt3.png'), 7),
        scale_image(pygame.image.load('imgs/bolt4.png'), 7),
        scale_image(pygame.image.load('imgs/bolt5.png'), 7)
    ]
    return images

class Game:
    def __init__(self):
        self.images = load_images()
        self.setup_display()
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'START'
        self.player_name = ''
        self.player_car = PlayerCar(self.images['red_car'], (288, 175))
        self.lives = 5
        self.laps = []
        self.dash_active = False
        self.dash_timer = 0
        self.dash_duration = 60
        self.finish_position = (259, 350)  # Adiciona a posição de chegada
        self.timer = 0
        self.lap = 1
        self.max_laps = 2
        self.current_life_image = self.images['life'][0]
        self.init_music()
        self.fonts = {
            'title': pygame.font.Font('fonts/PixelifySans-Bold.ttf', 120),
            'common': pygame.font.Font('fonts/PixelifySans-Medium.ttf', 65)
        }
        
        # Reintegrando as máscaras de colisão
        self.track_border_mask = pygame.mask.from_surface(self.images['track_border'])
        self.finish_mask = pygame.mask.from_surface(self.images['finish'])
        self.dash_mask = pygame.mask.from_surface(self.images['dash'])

    def init_music(self):
        pygame.mixer.music.load('sound/soundtrack.mp3')
        pygame.mixer.music.play(-1)

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
                        self.state = 'PLAYING'
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        self.player_name += event.unicode
                elif self.state in ['GAME_OVER', 'FINISHED']:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_r and self.state == 'GAME_OVER' or self.state == 'FINISHED':
                        self.reset_game()

    def reset_game(self):
        self.player_car.reset()
        self.lives = 5
        self.current_life_image = self.images['life'][0]
        self.laps = []
        self.timer = 0
        self.lap = 1
        self.state = 'PLAYING'

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
                self.player_car.acceleration = 1
                self.player_car.max_vel = 15

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
                        self.state = 'FINISHED'

    def render(self):
        if self.state == 'START':
            self.window.blit(self.images['init_screen'], (0, 0))

        elif self.state == 'GET_NAME':
            self.window.fill(BLACK)
            self.render_text("Digite seu nome:", 'title', WHITE, -100)
            name_surface = self.fonts['common'].render(self.player_name, True, WHITE)
            name_rect = name_surface.get_rect(center=(self.width / 2, self.height / 2))
            self.window.blit(name_surface, name_rect)

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
            self.window.blit(self.images['game_over'], (0, 0))

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
