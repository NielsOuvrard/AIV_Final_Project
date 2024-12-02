'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description: Enemy class to represent an enemy in the game
 '''

from src.entities.entity import Entity


class Enemy(Entity):
    """
    Enemy class to represent an enemy in the game
    """
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__("assets/enemies.png", "assets/enemies.toml", position)
