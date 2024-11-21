'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:19:49
 # @ Description:
 '''
import pygame as pg

from src.config import SCREEN_WIDTH, FONT_NAME, FONT_SIZE, FONT_BUTTON_SIZE, COLOR_BLACK, COLOR_WHITE, COLOR_RED
from src.game_states import MainState, State
from src.entities.player import Player
from src.world.level import LevelHandler

class Button: # pylint: disable=too-many-arguments, too-many-positional-arguments
    """
    Button class to represent a button in the menu
    """
    def __init__(self,
                 position: tuple[int, int],
                 text: str,
                 font: pg.font.Font,
                 color_text: tuple[int, int, int],
                 color_hover: tuple[int, int, int]) -> None:
        self.font: pg.font.Font = font
        self.text_color = color_text
        self.hover_color = color_hover
        self.text: str = text
        self.image: pg.Surface = self.font.render(self.text, True, self.text_color)
        self.rect: pg.Rect = self.image.get_rect(center=position)
        self.hovered: bool = False

    def draw(self, screen: pg.Surface) -> None:
        if self.hovered:
            self.image = self.font.render(self.text, True, self.hover_color)
        else:
            self.image = self.font.render(self.text, True, self.text_color)
        screen.blit(self.image, self.rect)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

class GameMenu(State):
    """
    Game menu class to represent the game menu
    """
    def __init__(self) -> None:
        super().__init__()
        self.next_state: MainState | None = None
        self.level_handler = LevelHandler()
        self.player: Player = Player(self.level_handler.current_level.start_position)

    def update(self) -> None:
        self.player.animate(0.1)
        self.player.move_and_slide(self.level_handler.current_level)

    def draw(self, screen: pg.Surface) -> None:
        screen.fill(COLOR_BLACK)
        self.player.draw(screen)
        self.level_handler.draw(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.next_state = MainState.QUIT
        self.player.handle_event(event)

class MainMenu(State):
    """
    Main menu class to represent the main menu of the game
    """
    def __init__(self) -> None:
        super().__init__()
        self.title: str = "Main Menu"
        self.title_font: pg.font.Font = pg.font.Font(FONT_NAME, int(FONT_SIZE * 1.5))
        self.title_text: pg.Surface = self.title_font.render(self.title, True, COLOR_WHITE)
        self.title_text_rect: pg.Rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        self.play_button: Button = Button(
            (SCREEN_WIDTH // 2, 200),
            "Play",
            pg.font.Font(FONT_NAME, FONT_SIZE),
            COLOR_WHITE,
            COLOR_RED
        )
        self.quit_button: Button = Button(
            (SCREEN_WIDTH // 2, 300),
            "Quit",
            pg.font.Font(FONT_NAME, FONT_SIZE),
            COLOR_WHITE,
            COLOR_RED
        )

    def update(self) -> None:
        pass

    def draw(self, screen: pg.Surface) -> None:
        screen.fill(COLOR_BLACK)
        screen.blit(self.title_text, self.title_text_rect)
        self.play_button.draw(screen)
        self.quit_button.draw(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.next_state = MainState.QUIT
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.play_button.rect.collidepoint(event.pos):
                self.next_state = MainState.GAME
            elif self.quit_button.rect.collidepoint(event.pos):
                self.next_state = MainState.QUIT
        self.play_button.handle_event(event)
        self.quit_button.handle_event(event)

class Credits(State):
    """
    Credits class to represent the credits screen of the game
    """
    def __init__(self) -> None:
        super().__init__()
        self.title: str = "Credits"
        self.title_font: pg.font.Font = pg.font.Font(FONT_NAME, int(FONT_SIZE * 1.5))
        self.title_text: pg.Surface = self.title_font.render(self.title, True, COLOR_WHITE)
        self.title_text_rect: pg.Rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        self.credits: str = "Authors: \nNiels Ouvrard \nDiego Jiménez Ontiveros \nSantiago Arreola Munguia \n\nClass: \nAI in videogames"
        self.credits_font: pg.font.Font = pg.font.Font(FONT_NAME, int(FONT_BUTTON_SIZE * 0.8))
        self.credits_text: pg.Surface = self.credits_font.render(self.credits, True, COLOR_WHITE)
        self.credits_text_rect: pg.Rect = self.credits_text.get_rect(center=(SCREEN_WIDTH // 2, 250))

        self.quit_button: Button = Button(
            (40, 40),
            "Quit",
            pg.font.Font(FONT_NAME, FONT_BUTTON_SIZE),
            COLOR_WHITE,
            COLOR_RED
        )

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(COLOR_BLACK)
        screen.blit(self.title_text, self.title_text_rect)
        screen.blit(self.credits_text, self.credits_text_rect)
        self.quit_button.draw(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.next_state = MainState.MAIN_MENU
        self.quit_button.handle_event(event)
