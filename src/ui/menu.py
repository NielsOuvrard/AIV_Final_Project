'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:19:49
 # @ Description:
 '''
import pygame

from src.config import *
from src.game_states import MainState, State


class Button:
    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font, text_color: tuple[int, int, int], hover_color: tuple[int, int, int]):
        self.font: pygame.font.Font = font
        self.text_color: tuple[int, int, int] = text_color
        self.hover_color: tuple[int, int, int] = hover_color
        self.text: str = text
        self.image: pygame.Surface = self.font.render(self.text, True, self.text_color)
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))
        self.hovered: bool = False

    def draw(self, screen: pygame.Surface) -> None:
        if self.hovered:
            self.image = self.font.render(self.text, True, self.hover_color)
        else:
            self.image = self.font.render(self.text, True, self.text_color)
        screen.blit(self.image, self.rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

class gameMenu(State):
    def __init__(self):
        self.next_state: MainState | None = None

    def update(self) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COLOR_BLACK)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.next_state = MainState.QUIT

class mainMenu(State):
    def __init__(self):
        super().__init__()
        self.title: str = "Main Menu"
        self.title_font: pygame.font.Font = pygame.font.Font(FONT_NAME, int(FONT_SIZE * 1.5))
        self.title_text: pygame.Surface = self.title_font.render(self.title, True, COLOR_WHITE)
        self.title_text_rect: pygame.Rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        self.play_button: Button = Button(SCREEN_WIDTH // 2, 200, "Play", pygame.font.Font(FONT_NAME, FONT_SIZE), COLOR_WHITE, COLOR_RED)
        self.quit_button: Button = Button(SCREEN_WIDTH // 2, 300, "Quit", pygame.font.Font(FONT_NAME, FONT_SIZE), COLOR_WHITE, COLOR_RED)

    def update(self) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(COLOR_BLACK)
        screen.blit(self.title_text, self.title_text_rect)
        self.play_button.draw(screen)
        self.quit_button.draw(screen)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.next_state = MainState.QUIT
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.rect.collidepoint(event.pos):
                self.next_state = MainState.GAME
            elif self.quit_button.rect.collidepoint(event.pos):
                self.next_state = MainState.QUIT
        self.play_button.handle_event(event)
        self.quit_button.handle_event(event)
