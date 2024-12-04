'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:19:49
 # @ Description:
 '''
import time
import pygame as pg

from src.config import (
    SCREEN_WIDTH,
    FONT_NAME,
    FONT_SIZE,
    FONT_BUTTON_SIZE,
    COLOR_BLACK,
    COLOR_WHITE,
    COLOR_RED,
    TILE_SIZE
)
from src.entities.enemy import Enemy
from src.game_states import MainState, State
from src.entities.player import Player
from src.world.level import LevelHandler
from src.entities.collisions import handle_entity_collision

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
        x, y = self.level_handler.current_level.start_position
        self.player: Player = Player((x * TILE_SIZE, y * TILE_SIZE))
        self.enemies: list[Enemy] = [Enemy(pos, self.player) for pos in self.level_handler.current_level.enemies]

    def update(self) -> None:
        self.player.animate(0.1)
        self.player.move_and_slide(self.level_handler.current_level)
        for enemy in self.enemies:
            enemy.update(0.1, self.level_handler.current_level, self.player)
        handle_entity_collision(self.level_handler.current_level, self.player.position, self.player.image, self.enemies)

    def draw(self, screen: pg.Surface) -> None:
        screen.fill(COLOR_BLACK)
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        self.level_handler.draw(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.next_state = MainState.QUIT
        if self.level_handler.game_over:
            self.next_state = MainState.DEATH
        elif self.level_handler.current_level.finished:
            if self.level_handler.level_number == len(self.level_handler.levels)-1:
                time.sleep(0.5)
            else:
                time.sleep(2)
            self.level_handler.next_level()
            self.player.position = pg.Vector2(self.level_handler.current_level.start_position[0] * TILE_SIZE, self.level_handler.current_level.start_position[1] *TILE_SIZE)
            self.enemies: list[Enemy] = [Enemy(pos, self.player) for pos in self.level_handler.current_level.enemies]
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
        self.credits_button: Button = Button(
            (SCREEN_WIDTH // 2, 300),
            "Credits",
            pg.font.Font(FONT_NAME, FONT_SIZE),
            COLOR_WHITE,
            COLOR_RED
        )
        self.quit_button: Button = Button(
            (SCREEN_WIDTH // 2, 400),
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
        self.credits_button.draw(screen)
        self.quit_button.draw(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.next_state = MainState.QUIT
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.play_button.rect.collidepoint(event.pos):
                self.next_state = MainState.INSTRUCTIONS
            elif self.quit_button.rect.collidepoint(event.pos):
                self.next_state = MainState.QUIT
            elif self.credits_button.rect.collidepoint(event.pos):
                self.next_state = MainState.CREDITS
        self.play_button.handle_event(event)
        self.quit_button.handle_event(event)
        self.credits_button.handle_event(event)

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

        self.credits: str = "Authors: \nNiels Ouvrard \nDiego Jiménez Ontiveros \nSantiago Arreola Munguia \n\n"
        self.credits += "Class: \nAI in videogames \n\nTeacher: \nAlfredo Emmanuel Garcia Falcon \n\n"
        self.credits += "Universidad Panamericana, Guadalajara, Jal."

        self.credits_font: pg.font.Font = pg.font.Font(FONT_NAME, int(FONT_BUTTON_SIZE))
        self.credits_text: pg.Surface = self.credits_font.render(self.credits, True, COLOR_WHITE)
        self.credits_text_rect: pg.Rect = self.credits_text.get_rect(center=(SCREEN_WIDTH // 2, 250))

        self.exit_button: Button = Button(
            (40, 40),
            "Exit",
            pg.font.Font(FONT_NAME, FONT_BUTTON_SIZE),
            COLOR_WHITE,
            COLOR_RED
        )

    def update(self) -> None:
        pass

    def draw(self, screen: pg.Surface) -> None:
        screen.fill(COLOR_BLACK)
        screen.blit(self.title_text, self.title_text_rect)
        screen.blit(self.credits_text, self.credits_text_rect)
        self.exit_button.draw(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.QUIT:
            self.next_state = MainState.QUIT
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.exit_button.rect.collidepoint(event.pos):
                self.next_state = MainState.MAIN_MENU
        self.exit_button.handle_event(event)

class Instructions(State):
    """
    Intructions class to represent the intructios screen of the game
    """
    def __init__(self) -> None:
        super().__init__()
        self.title: str = "Instructions"
        self.title_font: pg.font.Font = pg.font.Font(FONT_NAME, int(FONT_SIZE * 1.5))
        self.title_text: pg.Surface = self.title_font.render(self.title, True, COLOR_WHITE)
        self.title_text_rect: pg.Rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        self.instructions: str = "Help Mario find the shortest way out without getting captured!"
        self.instructions_font: pg.font.Font = pg.font.Font(FONT_NAME, int(FONT_BUTTON_SIZE))
        self.instructions_text: pg.Surface = self.instructions_font.render(self.instructions, True, COLOR_WHITE)
        self.instructions_text_rect: pg.Rect = self.instructions_text.get_rect(center=(SCREEN_WIDTH // 2, 200))

        self.controls: str = "Use the keyboard arrows to move & the space bar to JUMP!"
        self.controls_font: pg.font.Font = pg.font.Font(FONT_NAME, int(FONT_BUTTON_SIZE))
        self.controls_text: pg.Surface = self.controls_font.render(self.controls, True, COLOR_WHITE)
        self.controls_text_rect: pg.Rect = self.controls_text.get_rect(center=(SCREEN_WIDTH // 2, 250))

        self.start_button: Button = Button(
            (SCREEN_WIDTH//2, 400),
            "Start",
            pg.font.Font(FONT_NAME, FONT_SIZE),
            COLOR_WHITE,
            COLOR_RED
        )

        self.back_button: Button = Button(
            (40, 40),
            "Back",
            pg.font.Font(FONT_NAME, FONT_BUTTON_SIZE),
            COLOR_WHITE,
            COLOR_RED
        )

    def update(self) -> None:
        pass

    def draw(self, screen: pg.Surface) -> None:
        screen.fill(COLOR_BLACK)
        screen.blit(self.title_text, self.title_text_rect)
        screen.blit(self.instructions_text, self.instructions_text_rect)
        screen.blit(self.controls_text, self.controls_text_rect)
        self.start_button.draw(screen)
        self.back_button.draw(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == MainState.QUIT:
            self.next_state = MainState.MAIN_MENU
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.start_button.rect.collidepoint(event.pos):
                self.next_state = MainState.GAME
            if self.back_button.rect.collidepoint(event.pos):
                self.next_state = MainState.MAIN_MENU
        self.start_button.handle_event(event)
        self.back_button.handle_event(event)

class Death(State):
    def __init__(self) -> None:
        super().__init__()
        self.title: str = "You Died"
        self.title_font: pg.font.Font = pg.font.Font(FONT_NAME, int(FONT_SIZE * 1.5))
        self.title_text: pg.Surface = self.title_font.render(self.title, True, COLOR_RED)
        self.title_text_rect: pg.Rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))

        self.play_button: Button = Button(
            (SCREEN_WIDTH//2, 300),
            "Play Again",
            pg.font.Font(FONT_NAME, FONT_SIZE),
            COLOR_WHITE,
            COLOR_RED
        )

        self.back_button: Button = Button(
            (SCREEN_WIDTH//2, 400),
            "Back to menu",
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
        self.back_button.draw(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == MainState.QUIT:
            self.next_state = MainState.MAIN_MENU
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.play_button.rect.collidepoint(event.pos):
                self.next_state = MainState.GAME
            if self.back_button.rect.collidepoint(event.pos):
                self.next_state = MainState.MAIN_MENU
        self.play_button.handle_event(event)
        self.back_button.handle_event(event)
