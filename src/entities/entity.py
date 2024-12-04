'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description: Entity
 '''

import pygame as pg
import toml

from src.config import SCALING_FACTOR, GRAVITY
from src.world.level import Level
from src.entities.collisions import handle_collision


class Entity(pg.sprite.Sprite):
    """
    Entity class to represent a player, enemy, or any element having an animated sprite and collisions
    """
    def __init__(self, path_image: str, toml_path: str, position: tuple[int, int]) -> None:
        super().__init__()

        self.sprite_sheet = pg.image.load(path_image).convert_alpha()
        self.animations: dict = {}
        self.current_animation = 'idle'
        self.animation_speed = 0.1
        self.animation_time = 0.0
        self.frame_index = 0
        self.load_animations(toml_path)

        self.position = pg.Vector2(*position)
        self.velocity = pg.Vector2(0, 0)
        self.acceleration = pg.Vector2(0, 0)

        self.image: pg.Surface = self.animations[self.current_animation][self.frame_index]

    def get_frame(self, sprite_sheet: pg.Surface, position: tuple[int, int], size: tuple[int, int]) -> pg.Surface:
        frame = pg.Surface(size, pg.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (*position, *size))
        return frame

    def load_animations(self, toml_path: str):
        """
        Load animations from a TOML file
        """
        config = toml.load(toml_path)
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

    def move_and_slide(self, level: Level) -> None:
        """
        Move the player character and apply gravity
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

        handle_collision(level, self.position, self.image, self.velocity)

    def animate(self, dt: float):
        """
        Animate the player character sprite
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
