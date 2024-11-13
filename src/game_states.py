'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:32:22
 # @ Description:
 '''
from src.config import *
from enum import Enum

class MainState(Enum):
    MAIN_MENU = 0
    GAME = 1
    QUIT = 2

class State:
    def __init__(self):
        self.next_state = None

    def update(self):
        pass

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass