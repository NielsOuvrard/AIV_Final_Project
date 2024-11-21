'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-12-02 23:37
 # @ Description:
 '''

from enum import Enum
import pygame as pg
import toml
from src.config import SCALING_FACTOR, GRAVITY, TILE_SIZE
from src.world.level import Level
from player import CornerSide, ObjectCollision

class EnemyState(Enum):
  IDLE = 1
  PURSUE = 2
  DEATH = 3

class Enemy(pg.sprite.Sprite):
    """
    Enemy class to represent an enemy in the game
    """
    def __init__(self, position: tuple[int,int]) -> None:
        super().__init__()

        self.sprite_sheet = pg.image.load("assets/enemies.png").convert_alpha()
        self.animations: dict = {}
        self.current_animation: str = 'idle'
        self.animation_speed = 0.1
        self.animation_time=0.0
        self.frame_index = 0
        self.load_animations()

        self.position = pg.Vector2(*position)
        self.velocity = pg.Vector2(0,0)
        self.acceleration = pg.Vector2(0,0)

        self.image: pg.Surface = self.animations[self.current_animation][self.frame_index]

        self.actual_state = EnemyState.IDLE
        self.target = None
    
    def get_frame(self, sprite_sheet: pg.Surface, position: tuple[int, int], size: tuple[int, int]) -> pg.Surface:
        frame = pg.Surface(size, pg.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (*position, *size))
        return frame

    def load_animations(self):
        """
        Load animations from a TOML file
        """
        config = toml.load('assets/enemies.toml')
        frame_width = config['animations']['frame_width']
        frame_height = config['animations']['frame_height']

        for animation_name, animation_data in config['animations'].items():
            if animation_name in {'frame_width', 'frame_height'}:
                continue

            _ = animation_data['frame_count']
            y_position = animation_data['y_position']
            x_positions = animation_data['x_positions']

            frames = []
            for x in x_positions:
                frame = self.get_frame(self.sprite_sheet, (x, y_position), (frame_width, frame_height))
                frames.append(frame)
            self.animations[animation_name] = frames

    def snap_position(self, sides: set[CornerSide], objects: list[ObjectCollision]) -> None:
        """
        Snap the enemy position to the object it is colliding with
        """

        if {CornerSide.BOTTOM_LEFT, CornerSide.BOTTOM_RIGHT}.issubset(sides):
            self.position.y = objects[0].y - self.image.get_height() * SCALING_FACTOR
            self.velocity.y = 0
            self.change_animation('idle' if self.velocity.x == 0 else 'walk')
        elif {CornerSide.TOP_LEFT, CornerSide.BOTTOM_LEFT}.issubset(sides):
            self.position.x = objects[0].x + objects[0].size_x
            self.velocity.x = 0
        elif {CornerSide.TOP_RIGHT, CornerSide.BOTTOM_RIGHT}.issubset(sides):
            self.position.x = objects[0].x - self.image.get_width() * SCALING_FACTOR
            self.velocity.x = 0
        elif {CornerSide.TOP_LEFT, CornerSide.TOP_RIGHT}.issubset(sides):
            self.position.y = objects[0].y + objects[0].size_y
            self.velocity.y = GRAVITY


    def handle_collision(self, level: Level):
        """
        Handle collision with the level
        """
        enemy = ObjectCollision(
            self.position.x,
            self.position.y,
            self.image.get_width() * SCALING_FACTOR,
            self.image.get_height() * SCALING_FACTOR
        ) # 100.0, 546.0 with size 32, 32

        sides_colliding: set[CornerSide] = set()
        objects_colliding = []

        for tile in level.tiles:
            object_to_collide = ObjectCollision(
                tile.rect.x,
                tile.rect.y,
                TILE_SIZE,
                TILE_SIZE
            )
            local_colliding = enemy.is_colliding(object_to_collide)
            if local_colliding != set():
                sides_colliding.update(local_colliding)
                objects_colliding.append(object_to_collide)
                tile.color = (0, 0, 255)
        if sides_colliding != set():
            self.snap_position(sides_colliding, objects_colliding)

    def move_and_slide(self, level: Level):
        """
        Move the enemy character
        """
        # Update velocity with acceleration
        self.velocity += self.acceleration

        # Apply friction to slow down the player when not accelerating
        self.velocity.x *= 0.9

        # Update position with velocity
        self.position += self.velocity

        # Apply gravity
        self.acceleration.y = 0
        self.velocity.y += GRAVITY

        # Check for idle state
        if self.velocity.x < 0.01 and self.velocity.x > -0.01:
            self.change_animation('idle')
            self.velocity.x = 0

        self.handle_collision(level)

    def animate(self, dt: float):
        """
        Animate the enemy character sprite
        """
        # Update animation time
        self.animation_time += dt

        # Change frame when enough time has passed
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0
            self.frame_index += 1

            # Loop back to start of animation
            if self.frame_index >= len(self.animations[self.current_animation]):
                self.frame_index = 0

            # Update sprite image
            self.image = self.animations[self.current_animation][self.frame_index]

    def change_animation(self, animation_name: str):
        self.current_animation = animation_name
        self.frame_index = 0

    def draw(self, screen: pg.Surface):
        if self.velocity.x < 0:
            self.image = pg.transform.flip(self.image, True, False)
        else:
            self.image = pg.transform.flip(self.image, False, False)
        screen.blit(pg.transform.scale(self.image,
                                          (self.image.get_width() * SCALING_FACTOR,
                                           self.image.get_height() * SCALING_FACTOR)),
                   (self.position.x, self.position.y))
