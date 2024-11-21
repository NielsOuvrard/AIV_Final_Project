'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 17:26:06
 # @ Description:
 '''

import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE
from src.ui.menu import MainMenu, GameMenu, Credits
from src.game_states import MainState, State


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    actualState: State = MainMenu()

    running: bool = True
    while running:
        for event in pygame.event.get():
            actualState.handle_event(event)

        actualState.update()
        actualState.draw(screen)

        if actualState.next_state == MainState.GAME:
            actualState = GameMenu()
        elif actualState.next_state == MainState.MAIN_MENU:
            actualState = MainMenu()
        elif actualState.next_state == MainState.QUIT:
           # running = False # pylint: disable=invalid-name
            actualState = Credits()

        pygame.display.flip()

    pygame.quit()
