'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 17:26:06
 # @ Description:
 '''

import pygame
from src.config import *
from src.ui.menu import mainMenu, gameMenu
from src.game_states import MainState, State


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    actualState: State = mainMenu()

    running: bool = True
    while running:
        for event in pygame.event.get():
            actualState.handle_event(event)

        actualState.update()
        actualState.draw(screen)

        if actualState.next_state == MainState.GAME:
            actualState = gameMenu()
        elif actualState.next_state == MainState.MAIN_MENU:
            actualState = mainMenu()
        elif actualState.next_state == MainState.QUIT:
            running = False

        pygame.display.flip()

    pygame.quit()