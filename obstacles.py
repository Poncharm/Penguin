import pygame
import random

class Obstacles:
    def __init__(self, coin_width, screen, game_speed, WIDTH, HEIGHT, font):
        self.coin_width = coin_width
        self.screen = screen
        self.game_speed = game_speed
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.font = font
        self.coin_list = []
        self.score = 0

        self._load_coin_image()

    def _load_coin_image(self):
        """Загрузка изображения монеты и настройка прозрачности."""
        coin_image_path = 'Resources\\pics\\Rubble.png'
        self.coin_image = pygame.image.load(coin_image_path)
        self.coin_image = pygame.transform.scale(self.coin_image, (self.coin_width, self.coin_width)).convert()
        colorkey = self.coin_image.get_at((0, 0))
        self.coin_image.set_colorkey(colorkey)
        self.coin_sound_path = 'Resources/sounds/3.mp3'
        self.coin_sound = pygame.mixer.Sound(self.coin_sound_path)
        self.coin_sound.set_volume(0.4)  # установите громкость на ...%

    def draw_coin(self):
        """Отрисовка монет на экране."""
        for coin in self.coin_list:
            self.screen.blit(self.coin_image, coin.topleft)

    def generate_coin(self):
        """Создание монеты с учетом вероятности, зависящей от положения монеты по оси Y."""
        coin_x = random.randint(self.WIDTH, self.WIDTH + 100)
        coin_y = random.randint(0, self.HEIGHT - 200)

        chance = max(0, min(100, 100 * (1 - coin_y / self.HEIGHT)))

        if random.randint(1, 100) < chance:
            new_coin = pygame.Rect(coin_x, coin_y, self.coin_width, self.coin_width)
            self.coin_list.append(new_coin)

    def move_coin(self, background_shift_y):
        """Перемещение монет влево со скоростью игры и вертикальное перемещение на основе смещения фона."""
        for coin in self.coin_list:
            coin.x -= self.game_speed
            coin.y += background_shift_y  # Update the coin's y position based on the background shift
            if coin.x < -coin.width - self.coin_width:
                self.coin_list.remove(coin)

    def check_coin_collection(self, player):
        """Проверка на столкновение игрока с монетами."""
        for i in range(len(self.coin_list) - 1, -1, -1):
            coin = self.coin_list[i]
            if player.colliderect(coin):
                self.score += 1
                del self.coin_list[i]
                self.coin_sound.play()  # воспроизводим звук монетки при сборе

    def draw_score(self):
        """Отрисовка текущего счета на экране."""
        score_surface = self.font.render('Coins: ' + str(self.score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(topright=(self.WIDTH - 10, 10))
        self.screen.blit(score_surface, score_rect)
