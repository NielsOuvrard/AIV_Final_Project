'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:32:22
 # @ Description:
 '''

import pygame
from src.config import *
from enum import Enum

class MainState(Enum):
    MAIN_MENU = 0
    GAME = 1
    QUIT = 2

class State:
    def __init__(self):
        self.next_state: MainState | None = None

    def update(self) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        pass