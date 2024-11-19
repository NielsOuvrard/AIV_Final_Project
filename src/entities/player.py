'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description:
 '''

from enum import Enum
import pygame as pg
import toml
from src.config import SCALING_FACTOR, GRAVITY, TILE_SIZE
from src.world.level import Level

class CornerSide(Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3

class ObjectCollision:
    """
    ObjectCollision class to represent an object that can collide with other objects
    It can be a tile, a player, an enemy, etc...
    """
    def __init__(self, x: float, y: float, size_x: int, size_y: int):
        """
        The x and y coordinates are the top-left corner of the object
        """
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y

    def check_collision(self, point: pg.Vector2) -> bool:
        return (self.x <= point.x <= (self.x + self.size_x) and
                self.y <= point.y <= (self.y + self.size_y))

    def get_corners(self) -> list[pg.Vector2]:
        """
        Get the corners of the object
        In the order of: top-left, top-right, bottom-left, bottom-right
        """
        return [
            pg.Vector2(self.x, self.y),
            pg.Vector2(self.x + self.size_x, self.y),
            pg.Vector2(self.x, self.y + self.size_y),
            pg.Vector2(self.x + self.size_x, self.y + self.size_y)
        ]

    def is_colliding(self, other: 'ObjectCollision') -> set[CornerSide]:
        """
        Check if the object is colliding with another object
        """
        colliding = set()

        # for each corner of the player, check if it collides with the object
        for i, corner in enumerate(self.get_corners()):
            if other.check_collision(corner):
                colliding.add(CornerSide(i))

        return colliding

class Player(pg.sprite.Sprite):
    """
    Player class to represent the player character
    """
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__()

        self.sprite_sheet = pg.image.load("assets/mario_bros.png").convert_alpha()
        self.animations: dict = {}
        self.current_animation = 'idle'
        self.animation_speed = 0.1
        self.animation_time = 0.0
        self.frame_index = 0
        self.load_animations()

        self.position = pg.Vector2(*position)
        self.velocity = pg.Vector2(0, 0)
        self.acceleration = pg.Vector2(0, 0)

        self.image: pg.Surface = self.animations[self.current_animation][self.frame_index]

    def get_frame(self, sprite_sheet: pg.Surface, position: tuple[int, int], size: tuple[int, int]) -> pg.Surface:
        frame = pg.Surface(size, pg.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (*position, *size))
        return frame

    def load_animations(self):
        """
        Load animations from a TOML file
        """
        config = toml.load('assets/mario_bros.toml')
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
        Snap the player position to the object it is colliding with
        """
        # pylint: disable=fixme
        # todo see how to choose the right object

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
        player = ObjectCollision(
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
            local_colliding = player.is_colliding(object_to_collide)
            if local_colliding != set():
                sides_colliding.update(local_colliding)
                objects_colliding.append(object_to_collide)
                tile.color = (0, 0, 255)
        if sides_colliding != set():
            self.snap_position(sides_colliding, objects_colliding)

    def move_and_slide(self, level: Level):
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

        self.handle_collision(level)

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

    def draw(self, screen: pg.Surface):
        if self.velocity.x < 0:
            self.image = pg.transform.flip(self.image, True, False)
        else:
            self.image = pg.transform.flip(self.image, False, False)
        screen.blit(pg.transform.scale(self.image,
                                          (self.image.get_width() * SCALING_FACTOR,
                                           self.image.get_height() * SCALING_FACTOR)),
                   (self.position.x, self.position.y))
