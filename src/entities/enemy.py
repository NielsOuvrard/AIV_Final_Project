'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description: Enemy class to represent an enemy in the game
 '''

from enum import Enum
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
    DEAD = 4

class Enemy(Entity):
    """
    Enemy class with state machine implementation.
    """
    def __init__(self, position: tuple[int, int], player: Player) -> None:
        super().__init__("assets/enemies.png", "assets/enemies.toml", position)
        self.entity:str = "Enemy"
        self.target = player
        self.state = EnemyState.IDLE
        self.health = 1

    def change_state(self, new_state: EnemyState):
        """
        Change the current state of the enemy.
        """
        if self.state != new_state:  # Avoid redundant state changes
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
            self.update_attacking()
        elif self.state == EnemyState.DEAD:
            self.update_dead()

        self.animate(dt)
        super().move_and_slide(level, self.entity)

    def update_idle(self):
        """
        Behavior for the IDLE state.
        """
        if self.target_in_range(5*TILE_SIZE):
            self.change_state(EnemyState.WALKING)

    def update_walking(self, player: Player):
        """
        Behavior for the WALKING state.
        """
        direction = player.position - self.position
        if direction.x > 0:
            self.acceleration.x = 0.015
        else:
            self.acceleration.x = -0.015
        if self.target_in_range(2):
            self.change_state(EnemyState.ATTACKING)

    def update_attacking(self):
        """
        Behavior for the ATTACKING state.
        """

        if not self.target_in_range(7):
            self.change_state(EnemyState.WALKING)

    def update_dead(self):
        """
        Behavior for the DEAD state.
        """
        self.current_animation = 'die'

    def target_in_range(self, range_distance: int) -> bool:
        """
        Check if the target (player) is within a certain distance.
        """
        if self.target:
            return (self.target.position - self.position).length() < range_distance
        return False
