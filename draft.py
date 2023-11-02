# External libs
import pygame

# Internal modules
from game_settings import *


class Background():
    def __init__(self, screen, width, height):
        """Initialize the background properties."""
        self.width = width
        self.height = height
        self.screen = screen
        self.layers = []
        self.layer_x_positions = []
        self.layer_speeds = []

        # Initialize x and y attributes
        self.x = 0

    def display_lsl_info(self, lsl_value=None, lsl_channel_name="LSL Channel"):
        """Display the current LSL value on the screen."""
        if lsl_value is not None:
            font = pygame.font.SysFont('freesansbold.ttf', 24)
            value_text = font.render(f"{lsl_channel_name}: {lsl_value:.2f}", True, (255, 255, 255))
            self.screen.blit(value_text, (10, 10))

    def draw_screen(self):
        """Draw the screen with multiple layers."""
        self.screen.fill((0, 0, 0))

        for i, layer in enumerate(self.layers):
            layer_width = layer.get_width()

            # Calculate how many copies of the layer are needed to cover the entire screen width
            num_copies = (self.width + layer_width - 1) // layer_width + 1

            # Draw the required number of layer copies, accounting for y position
            for j in range(num_copies):
                self.screen.blit(layer, (self.layer_x_positions[i] + j * layer_width, self.y))

            self.layer_x_positions[i] -= self.layer_speeds[i]

            # Update the layer position when it completely goes off the screen
            if self.layer_x_positions[i] <= -layer_width:
                self.layer_x_positions[i] += layer_width

        return self.layer_x_positions

    def initialize_forest(self, path):
        """Load and initialize a forest with multiple layers."""
        # Load the layers
        self.layers = [
            pygame.image.load(
                f"{path}/Layer_{str(i).zfill(4)}.png").convert_alpha()
            for i in range(12)
        ]
        self.layers.reverse()
        self.layer_x_positions = [0 for _ in range(12)]
        self.layer_speeds = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4]  # Sample speeds, can be adjusted

        for i, layer in enumerate(self.layers):
            # Scale each layer
            self.layers[i] = pygame.transform.scale(layer, (self.width, self.height))

    def initialize_sky(self, path):
        """Load and initialize a sky with multiple layers."""
        # Load the layers
        self.layers = [pygame.image.load(f"{path}/sunsetbackground.png").convert_alpha()]
        self.layers.reverse()
        self.layer_x_positions = [0 for _ in range(12)]
        self.layer_speeds = [0.2]  # Sample speeds, can be adjusted

        for i, layer in enumerate(self.layers):
            # Scale each layer
            self.layers[i] = pygame.transform.scale(layer, (self.width, self.height))

