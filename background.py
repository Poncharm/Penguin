# External libs
import pygame

class Background():
    def __init__(self, screen, width, height):
        """Initialize the background properties."""
        self.width = width
        self.height = height
        self.screen = screen

        # Initial x and y attributes
        self.x = 0

        # Dict to store layers' y-positions
        self.y = {'forest': 0,
                  'sky1': -1*self.height,
                  'sky2': -2*self.height,
                  'sky3': -3*self.height,
                  'sky4': -4*self.height,
                  'sky5': -5*self.height}

        # Initialize attributes for both forest and sky
        self.init_attributes('forest')
        self.init_attributes('sky1')
        self.init_attributes('sky2')
        self.init_attributes('sky3')
        self.init_attributes('sky4')
        self.init_attributes('sky5')

    def init_attributes(self, prefix):
        setattr(self, f"{prefix}_layers", [])
        setattr(self, f"{prefix}_layer_x_positions", [])
        setattr(self, f"{prefix}_layer_speeds", [])

    def display_lsl_info(self, lsl_value=None, lsl_channel_name="LSL Channel"):
        """Display the current LSL value on the screen."""
        if lsl_value is not None:
            font = pygame.font.SysFont('freesansbold.ttf', 24)
            value_text = font.render(f"{lsl_channel_name}: {lsl_value:.2f}", True, (255, 255, 255))
            self.screen.blit(value_text, (10, 10))

    def display_height(self, font, height=0):
        """Display the current LSL value on the screen."""
        score_surface = font.render(f"Height: {height:.0f}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(topright=(self.width - 200, 10))
        self.screen.blit(score_surface, score_rect)

    def draw_screen(self):
        """Draw the screen with multiple layers."""
        self.screen.fill((0, 0, 0))
        self.draw_layers('forest')
        self.draw_layers('sky1')
        self.draw_layers('sky2')
        self.draw_layers('sky3')
        self.draw_layers('sky4')
        self.draw_layers('sky5')

    def draw_layers(self, prefix):
        layers = getattr(self, f"{prefix}_layers")
        layer_x_positions = getattr(self, f"{prefix}_layer_x_positions")
        layer_speeds = getattr(self, f"{prefix}_layer_speeds")

        for i, layer in enumerate(layers):
            layer_width = layer.get_width()
            num_copies = (self.width + layer_width - 1) // layer_width + 1

            for j in range(num_copies):
                self.screen.blit(layer, (layer_x_positions[i] + j * layer_width, self.y[prefix]))

            layer_x_positions[i] -= layer_speeds[i]
            if layer_x_positions[i] <= -layer_width:
                layer_x_positions[i] += layer_width

    def initialize_forest(self, path):
        """Load and initialize a forest with multiple layers."""
        self.init_layers(path, 'forest', 11, [0.2 * i for i in range(1, 13)])

    def initialize_sky1(self, path):
        """Load and initialize a sky with multiple layers."""
        self.init_layers(path, 'sky1', 4, [0.2 * i for i in range(1, 5)])
    def initialize_sky2(self, path):
        """Load and initialize a sky with multiple layers."""
        self.init_layers(path, 'sky2', 4, [0.2 * i for i in range(1, 5)])
    def initialize_sky3(self, path):
        """Load and initialize a sky with multiple layers."""
        self.init_layers(path, 'sky3', 4, [0.2 * i for i in range(1, 5)])
    def initialize_sky4(self, path):
        """Load and initialize a sky with multiple layers."""
        self.init_layers(path, 'sky4', 4, [0.2 * i for i in range(1, 5)])
    def initialize_sky5(self, path):
        """Load and initialize a sky with multiple layers."""
        self.init_layers(path, 'sky5', 4, [0.2 * i for i in range(1, 5)])

    def init_layers(self, path, prefix, num_layers, speeds):
        if prefix == 'forest':
            layers = [pygame.image.load(f"{path}/Layer_{str(i).zfill(4)}.png").convert_alpha() for i in range(num_layers)]
            layers.reverse()
        elif prefix == 'sky1':
            layers = [pygame.image.load(f"{path}/{i}.png").convert_alpha() for i in range(1, 5)]
        elif prefix == 'sky2':
            layers = [pygame.image.load(f"{path}/{i}.png").convert_alpha() for i in range(1, 5)]
        elif prefix == 'sky3':
            layers = [pygame.image.load(f"{path}/{i}.png").convert_alpha() for i in range(1, 5)]
        elif prefix == 'sky4':
            layers = [pygame.image.load(f"{path}/{i}.png").convert_alpha() for i in range(1, 5)]
        elif prefix == 'sky5':
            layers = [pygame.image.load(f"{path}/{i}.png").convert_alpha() for i in range(1, 5)]

        # Set the attributes for the given prefix
        setattr(self, f"{prefix}_layers", layers)
        setattr(self, f"{prefix}_layer_x_positions", [0 for _ in range(num_layers)])
        setattr(self, f"{prefix}_layer_speeds", speeds)

        for i, layer in enumerate(layers):
            layers[i] = pygame.transform.scale(layer, (self.width, self.height))