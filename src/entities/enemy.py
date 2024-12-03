'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description: Enemy class to represent an enemy in the game
 '''

from src.entities.entity import Entity
from src.entities.player import Player
from enum import Enum
import pygame as pg

class EnemyState(Enum):
    """ 
    Enum to represent the state of an enemy 
    """
    IDLE = 1
    WALKING = 2
    ATTACKING = 3
    DEAD = 4

class Enemy(Entity):
    """
    Enemy class with state machine implementation.
    """
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__("assets/enemies.png", "assets/enemies.toml", position)
        self.target: Player = None
        self.state = EnemyState.IDLE  
        self.health = 1

    def change_state(self, new_state: EnemyState):
        """
        Change the current state of the enemy.
        """
        if self.state != new_state:  # Avoid redundant state changes
            print(f"Transitioning from {self.state} to {new_state}")
            self.state = new_state

    def update(self, dt: float, level, player: Player):
        """
        Update the enemy's behavior based on its current state.
        """
        if self.state == EnemyState.IDLE:
            self.update_idle()
        elif self.state == EnemyState.WALKING:
            self.update_walking(player)
        elif self.state == EnemyState.ATTACKING:
            self.update_attacking(player)
        elif self.state == EnemyState.DEAD:
            self.update_dead()

        self.animate(dt)
        self.move_and_slide(level)

    def update_idle(self):
        """
        Behavior for the IDLE state.
        """
        self.change_animation('idle')
        if self.target_in_range(30): 
            self.change_state(EnemyState.WALKING)

    def update_walking(self, player: Player):
        """
        Behavior for the WALKING state.
        """
        self.change_animation('walking')
        direction = player.position - self.position
        if direction.length() > 0:  
            direction.normalize_ip()
        self.velocity = direction * 2 

        if self.target_in_range(5):
            self.change_state(EnemyState.ATTACKING)

    def update_attacking(self, player: Player):
        """
        Behavior for the ATTACKING state.
        """
        self.change_animation('attacking')
        self.velocity = pg.Vector2(0, 0)  

        if self.target_in_range(5):
            player.take_damage(1)

        if not self.target_in_range(5):
            self.change_state(EnemyState.WALKING)

    def update_dead(self):
        """
        Behavior for the DEAD state.
        """
        self.current_animation = 'die'
        self.kill

    def target_in_range(self, range_distance: float) -> bool:
        """
        Check if the target (player) is within a certain distance.
        """
        if self.target:
            return (self.target.position - self.position).length() < range_distance
        return False

    def take_damage(self, amount: int):
        """
        Handle taking damage, possibly transitioning to DEAD state.
        """
        self.health -= amount
        if self.health <= 0:
            self.change_state(EnemyState.DEAD)

    