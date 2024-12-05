'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description: Enemy class to represent an enemy in the game
 '''

from enum import Enum
import pygame as pg

from src.entities.entity import Entity
from src.entities.player import Player
from src.config import TILE_SIZE

class EnemyState(Enum):
    """
    Enum to represent the state of an enemy
    """
    IDLE = 1
    WALKING = 2
    ATTACKING = 3
    DYING = 4

class Enemy(Entity):
    """
    Enemy class with state machine implementation.
    """
    def __init__(self, position: tuple[int, int], player: Player) -> None:
        super().__init__("assets/enemies.png", "assets/enemies.toml", position)
        self.state = EnemyState.IDLE
        self.target = player
        self.frame_remains = 1

    def change_state(self, new_state: EnemyState):
        """
        Change the current state of the enemy.
        """
        if self.state != new_state:  # Avoid redundant state changes
            self.state = new_state

    def kill(self):
        """
        Kill the enemy.
        """
        self.state = EnemyState.DYING
        self.change_animation('die')
        self.frame_remains = 60 * 5 # 5 seconds

    def update(self, dt: float, level) -> None:
        """
        Update the enemy's behavior based on its current state.
        """
        def target_in_range(range_distance: int) -> bool:
            """
            Check if the target (player) is within a certain distance.
            """
            if self.target:
                return (self.target.position - self.position).length() < range_distance
            return False

        def update_idle():
            if target_in_range(5 * TILE_SIZE):
                self.change_state(EnemyState.WALKING)

        def update_walking():
            direction = self.target.position - self.position
            if direction.x > 0:
                self.acceleration.x = 0.015
            else:
                self.acceleration.x = -0.02

            if target_in_range(2 * TILE_SIZE):
                self.change_state(EnemyState.ATTACKING)

        def update_attacking():
            # the attack state is only for the animation
            self.change_animation('attack')
            if not target_in_range(2 * TILE_SIZE):
                self.change_state(EnemyState.WALKING)

        if self.state == EnemyState.IDLE:
            update_idle()
        elif self.state == EnemyState.WALKING:
            update_walking()
        elif self.state == EnemyState.ATTACKING:
            update_attacking()
        elif self.state == EnemyState.DYING:
            self.frame_remains -= 1

        self.animate(dt)
        if not self.state == EnemyState.DYING:
            self.move_and_slide(level)
