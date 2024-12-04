'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description:
 '''

import pygame as pg

from src.entities.entity import Entity

class Player(Entity):
    """
    Player class to represent the player character
    """
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__("assets/mario_bros.png", "assets/mario_bros.toml", position)
        self.entity: str = "Player" 

    def handle_event(self, event: pg.event.Event):
        """
        Handle player character events
        Which are: jump, walk
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.change_animation('jump')
                self.acceleration.y = -5
            if event.key == pg.K_RIGHT:
                self.change_animation('walk')
                self.acceleration.x = 0.04
            if event.key == pg.K_LEFT:
                self.change_animation('walk')
                self.acceleration.x = -0.04
        if event.type == pg.KEYUP:
            if event.key in {pg.K_RIGHT, pg.K_LEFT}:
                self.acceleration.x = 0
                
    def move_and_slide(self, level):
        return super().move_and_slide(level, self.entity)