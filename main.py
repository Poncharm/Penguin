# Remaking Jetpack Joyride in Python!

# External libs
import random
import pygame

# Local modules
from lsl_handler import LSLHandler
from character import Character
from background import Background
from ui import UI
from obstacles import Obstacles
from game_settings import *

pygame.init()
pygame.mixer.init()

songs_list = [
    'Resources\\sounds\\1.mp3',
    'Resources\\sounds\\2.mp3',
    'Resources\\sounds\\3.mp3',
    'Resources\\sounds\\4.mp3'
]
current_song_index = 0

engine_sound_path = 'Resources/sounds/4.mp3'
engine_sound = pygame.mixer.Sound(engine_sound_path)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Jetpack Joyride Remake in Python!')
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

background = Background(screen, WIDTH, HEIGHT)
background.initialize_forest("Resources/background/forest")
background.initialize_sky1("Resources/background/clouds/clouds 1")
background.initialize_sky2("Resources/background/clouds/clouds 2")
background.initialize_sky3("Resources/background/clouds/clouds 3")
background.initialize_sky4("Resources/background/clouds/clouds 4")
background.initialize_sky5("Resources/background/clouds/clouds 5")

lsl_handler = LSLHandler()
user_interface = UI(screen, lsl_handler)

penguin = Character(screen, INIT_Y, init_x)
coin = Obstacles(coin_width, screen, game_speed, WIDTH, HEIGHT, font)

pygame.mixer.music.load(songs_list[current_song_index])
pygame.mixer.music.play()

last_keypress_time = 0
record = 0

while RUN:
    timer.tick(fps)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.KEYDOWN:
            current_time = pygame.time.get_ticks()
            if event.key == pygame.K_ESCAPE and current_time - last_keypress_time > KEYPRESS_DELAY:
                if GAME_STATE == 'game':
                    GAME_STATE = 'menu'
                elif GAME_STATE == 'menu':
                    GAME_STATE = 'game'
                last_keypress_time = current_time

    if GAME_STATE == 'game':
        if not pygame.mixer.music.get_busy():  # Если музыка не играет
            current_song_index += 1  # move to the next song
            if current_song_index >= len(songs_list):  # if we've reached the end of the list, start over
                current_song_index = 0
            pygame.mixer.music.load(songs_list[current_song_index])
            pygame.mixer.music.play()

        new_fire_rate = lsl_handler.get_current_fire_rate()
        if new_fire_rate is not None:
            fire_rate = new_fire_rate
            engine_sound.set_volume(fire_rate*0.8)  # Устанавливаем громкость звука двигателя на основе fire_rate

        # Counter Logic
        if counter < 40:
            counter += 1
        else:
            counter = 0

        # Booster Logic
        if not pause:
            if fire_rate > 0:
                booster = True
            else:
                booster = False

            if fire_rate >= 1:
                max_height = 0
            else:
                max_height = INIT_Y*(1 - fire_rate)

            if player_y > max_height + (fire_rate * 4 + 1):
                y_velocity = -fire_rate * 4

            elif player_y < max_height - (fire_rate * 4 + 1):
                y_velocity = (1 - fire_rate) * 4

            elif abs(player_y-max_height) <= fire_rate * 4 + 1:
                y_velocity = 0

            background_shift_y = 0
            if (player_y >= INIT_Y - HEIGHT//4) and (background.y['forest'] > 0):
                background_shift_y = -4

            elif player_y <= 20:
                background_shift_y = fire_rate * 4

            background.y['forest'] += background_shift_y
            background.y['sky1'] += background_shift_y
            background.y['sky2'] += background_shift_y
            background.y['sky3'] += background_shift_y
            background.y['sky4'] += background_shift_y
            background.y['sky5'] += background_shift_y

            player_y += y_velocity

        # Drawings
        background.draw_screen()
        background.display_lsl_info(lsl_value=fire_rate)

        if record < -(player_y - INIT_Y) + background.y['forest']: record = -(player_y - INIT_Y) + background.y['forest']
        background.display_height(font, record)

        player = penguin.draw_penguin(player_y, fire_rate, booster, background.y['forest'], INIT_Y, counter)

        # Coin Logic
        if random.randint(1, 100) <= COIN_GENERATION_CHANCE:
            coin.generate_coin()
        coin.move_coin(background_shift_y)  # pass the background shift to the move_coin method
        coin.check_coin_collection(player)
        coin.draw_coin()
        coin.draw_score()

    elif GAME_STATE == 'menu':
        pygame.mixer.music.pause()
        engine_sound.stop()
        RUN, CHANNEL = user_interface.draw_pause(events)
        if CHANNEL:  # Check if a new channel was selected
            lsl_handler.set_stream(CHANNEL)  # Set the new stream
            if not lsl_handler.is_running():  # Only start if it isn't already running
                lsl_handler.start()

    pygame.display.flip()

lsl_handler.stop()
pygame.quit()
