import pygame
import random
import math

class Character:
    def __init__(self, screen, init_y, init_x=170, scale=0.6):
        self.screen = screen
        self.scale = scale
        self.init_x = init_x/scale
        self.init_y = init_y
        self.fire_counter = 0

    def scale_value(self, val):
        return int(val * self.scale)

    def scale_list(self, list_of_values):
        return [self.scale_value(val) for val in list_of_values]

    def draw_feet(self, player_y, counter):
        foot_positions = [
            (self.scale_list([self.init_x-30, player_y + 90, 15, 5]), self.scale_list([self.init_x-35, player_y + 90, 15, 5])),
            (self.scale_list([self.init_x-35, player_y + 90, 20, 5]), self.scale_list([self.init_x-40, player_y + 90, 20, 5])),
            (self.scale_list([self.init_x-40, player_y + 90, 15, 5]), self.scale_list([self.init_x-45, player_y + 90, 15, 5])),
            (self.scale_list([self.init_x-30, player_y + 90, 15, 5]), self.scale_list([self.init_x-35, player_y + 90, 15, 5])),
        ]
        counter //= 10
        pygame.draw.ellipse(self.screen, 'yellow', foot_positions[counter % 4][0])
        pygame.draw.ellipse(self.screen, 'orange', foot_positions[counter % 4][1])

    def draw_penguin(self, player_y, fire_rate, booster, background_y, init_y, counter):
        player_y = player_y/self.scale + 95*(self.scale)

        penguin_body_position = self.scale_list([self.init_x - 50, player_y])
        penguin_body_size = self.scale_list([65, 90])
        play = pygame.rect.Rect(penguin_body_position, penguin_body_size)

        if background_y <= 5 and penguin_body_position[1] >= init_y - 5:
            self.draw_feet(player_y, counter)
        else:
            if booster:
                max_fire_length = int(30 * fire_rate * 4)

                # Using Gaussian (normal) distribution for smoother fire animations
                red_fire_length = int(random.gauss(max_fire_length * 0.75, max_fire_length * 0.1))
                orange_fire_length = int(random.gauss(max_fire_length * 0.55, max_fire_length * 0.1))
                yellow_fire_length = int(random.gauss(max_fire_length * 0.375, max_fire_length * 0.1))

                # Clamp the values to ensure they remain within the desired range
                red_fire_length = max(max_fire_length // 2, min(max_fire_length, red_fire_length))
                orange_fire_length = max(max_fire_length // 3, min(2 * max_fire_length // 3, orange_fire_length))
                yellow_fire_length = max(max_fire_length // 4, min(max_fire_length // 2, yellow_fire_length))

                pygame.draw.ellipse(self.screen, 'red',
                                    self.scale_list([self.init_x - 70, player_y + 70, 20, red_fire_length]))
                pygame.draw.ellipse(self.screen, 'orange', self.scale_list(
                    [self.init_x - 65, player_y + 70 + (max_fire_length - orange_fire_length) / 2, 10,
                     orange_fire_length]))
                pygame.draw.ellipse(self.screen, 'yellow', self.scale_list(
                    [self.init_x - 60, player_y + 70 + (max_fire_length - yellow_fire_length) / 2, 5,
                     yellow_fire_length]))

            pygame.draw.ellipse(self.screen, 'yellow', self.scale_list([self.init_x - 35, player_y + 90, 15, 5]))
            pygame.draw.ellipse(self.screen, 'orange', self.scale_list([self.init_x - 40, player_y + 90, 15, 5]))

        self.draw_penguin_body(player_y)
        return play

    def draw_penguin_body(self, player_y):
        # Main body details and improvements
        pygame.draw.ellipse(self.screen, 'black', self.scale_list([self.init_x-50, player_y + 20, 40, 70]))
        pygame.draw.ellipse(self.screen, 'white', self.scale_list([self.init_x-35, player_y + 35, 25, 40]))
        pygame.draw.arc(self.screen, 'grey', self.scale_list([self.init_x-40, player_y + 40, 30, 40]), math.pi, 2*math.pi, 1)  # Belly line for detail
        pygame.draw.ellipse(self.screen, 'black', self.scale_list([self.init_x-35, player_y + 5, 30, 30]))
        pygame.draw.circle(self.screen, 'white', tuple(self.scale_list([self.init_x-10, player_y + 15])), self.scale_value(4))
        pygame.draw.circle(self.screen, 'black', tuple(self.scale_list([self.init_x-8, player_y + 15])), self.scale_value(3))

        # Jetpack details and improvements
        pygame.draw.polygon(self.screen, 'orange', [tuple(self.scale_list(coords)) for coords in [(self.init_x, player_y + 15), (self.init_x-5, player_y + 17), (self.init_x-5, player_y + 13)]])
        pygame.draw.polygon(self.screen, 'darkgrey', [tuple(self.scale_list(coords)) for coords in [(self.init_x-65, player_y + 70), (self.init_x-55, player_y + 70), (self.init_x-48, player_y + 80), (self.init_x-72, player_y + 80)]])
        pygame.draw.rect(self.screen, 'grey', self.scale_list([self.init_x-75, player_y + 35, 30, 40]), 0, self.scale_value(5))
        pygame.draw.rect(self.screen, 'grey', self.scale_list([self.init_x-50, player_y + 60, 40, 5]), 0, self.scale_value(5))
        pygame.draw.rect(self.screen, 'grey', self.scale_list([self.init_x-10, player_y + 55, 5, 10]), 0, self.scale_value(5))
        pygame.draw.polygon(self.screen, 'black', [tuple(self.scale_list(coords)) for coords in [(self.init_x-45, player_y + 30), (self.init_x-25, player_y + 30), (self.init_x-17, player_y + 50), (self.init_x-2, player_y + 60), (self.init_x-23, player_y + 62)]])

        # Eye sparkle
        pygame.draw.circle(self.screen, 'white', tuple(self.scale_list([self.init_x-5, player_y + 13])), self.scale_value(1))

        # Jetpack badge/icon
        pygame.draw.circle(self.screen, 'blue', tuple(self.scale_list([self.init_x-60, player_y + 50])), self.scale_value(8))
        pygame.draw.circle(self.screen, 'white', tuple(self.scale_list([self.init_x-60, player_y + 50])), self.scale_value(6))
        pygame.draw.polygon(self.screen, 'yellow', [tuple(self.scale_list(coords)) for coords in [(self.init_x-63, player_y + 48), (self.init_x-57, player_y + 48), (self.init_x-60, player_y + 43)]])

        # Smoke/Steam when jetpack isn't active
        smoke_coords = [(self.init_x-63, player_y + 75), (self.init_x-58, player_y + 73), (self.init_x-60, player_y + 78)]
        pygame.draw.polygon(self.screen, 'lightgrey', [tuple(self.scale_list(coords)) for coords in smoke_coords])

        # Ribbon or streamers on the jetpack
        ribbon_coords = [(self.init_x-75, player_y + 35), (self.init_x-80, player_y + 25), (self.init_x-83, player_y + 15)]
        pygame.draw.lines(self.screen, 'red', False, [tuple(self.scale_list(coords)) for coords in ribbon_coords], self.scale_value(2))
