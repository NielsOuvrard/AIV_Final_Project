'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:32:22
 # @ Description:
 '''

from enum import Enum
import pygame

class MainState(Enum):
    """
    Enum class for the main states of the game.
    """
    MAIN_MENU = 0
    GAME = 1
    CREDITS = 2
    QUIT = 3
    INSTRUCTIONS = 4
    DEATH = 5

class State:
    """
    Base class for the game states.
    All methods should be overridden by subclasses to define the specific logic for the state.
    """
    def __init__(self):
        self.next_state: MainState | None = None

    def update(self) -> None:
        """
        Update the state.
        """

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the state to the screen.

        Args:
            screen (pygame.Surface): The surface to draw the state on.
        """

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle events for the state.

        Args:
            event (pygame.event.Event): The event to handle.
        """
