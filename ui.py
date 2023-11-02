import pygame
from game_settings import *

class UI():
    def __init__(self, screen, lsl_handler):
        self.screen = screen
        self.lsl_handler = lsl_handler
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.list_font = pygame.font.Font('freesansbold.ttf', 24)  # Меньший размер шрифта для элементов списка
        self.show_lsl_channels = False
        self.lsl_channels = self.lsl_handler.get_available_streams()
        self.selected_channel = None
        self.channel_changed = False  # Флаг, показывающий, был ли канал изменен

    def draw_button(self, text, x, y, w, h, color, hover_color, action=None, events=[]):
        mouse = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, hover_color, (x, y, w, h))
            if mouse_clicked and action is not None:
                action()
        else:
            pygame.draw.rect(self.screen, color, (x, y, w, h))

        btn_text = self.font.render(text, True, 'black')
        self.screen.blit(btn_text, (x + (w - btn_text.get_width()) // 2, y + (h - btn_text.get_height()) // 2))

    def draw_list_item(self, text, x, y, w, h, default_color, hover_color, selected_color, events=[]):
        mouse = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        item_color = default_color

        if text == self.selected_channel:
            item_color = selected_color
        elif x + w > mouse[0] > x and y + h > mouse[1] > y:
            item_color = hover_color
        pygame.draw.rect(self.screen, item_color, (x, y, w, h))

        if mouse_clicked and x + w > mouse[0] > x and y + h > mouse[1] > y:
            if self.selected_channel != text:
                self.selected_channel = text
                self.channel_changed = True  # Устанавливаем флаг, что канал был изменен
            self.lsl_handler.set_stream(text)  # Здесь устанавливаем выбранный канал в LSLHandler

        btn_text = self.list_font.render(text, True, 'black')  # Используем шрифт для элементов списка
        self.screen.blit(btn_text, (x + 40, y + (h - btn_text.get_height()) // 2))  # Немного сдвинули текст вправо

        pygame.draw.line(self.screen, 'black', (x, y + h), (x + w, y + h), 1)  # Разделительная линия

        circle_radius = 12  # Радиус кружка
        pygame.draw.circle(self.screen, 'black', (x + 20, y + h // 2), circle_radius, 2)  # Рисуем кружок

        # Если элемент списка выбран, рисуем внутри кружка стрелочку
        if text == self.selected_channel:
            pygame.draw.polygon(self.screen, 'black', [
                (x + 20 - circle_radius // 2, y + h // 2),
                (x + 20 + circle_radius // 2, y + h // 2),
                (x + 20, y + h // 2 - circle_radius // 2)
            ])

    def handle_lsl_channels(self):
        self.show_lsl_channels = not self.show_lsl_channels

    def handle_quit(self):
        global RUN
        RUN = False

    def draw_pause(self, events=[]):
        self.channel_changed = False  # Обнуляем флаг изменения канала при каждом вызове

        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, (128, 128, 128, 150), [0, 0, WIDTH, HEIGHT])
        pygame.draw.rect(surface, 'dark gray', [200, 150, 600, 50], 0, 10)
        surface.blit(self.font.render('Game Paused. Escape Btn Resumes', True, 'black'), (220, 160))

        self.draw_button('Quit', 360, 220, 280, 50, 'white', 'gray', self.handle_quit, events)
        self.draw_button('Update LSL', 360, 280, 280, 50, 'white', 'gray', self.handle_lsl_channels, events)

        if self.show_lsl_channels:
            for i, channel in enumerate(self.lsl_channels):
                y_position = 340 + i * 40
                self.draw_list_item(channel, 360, y_position, 280, 40, 'white', 'gray', 'green', events)

        self.screen.blit(surface, (0, 0))
        return RUN, self.selected_channel if self.channel_changed else None  # Возвращаем канал только если он был изменен
