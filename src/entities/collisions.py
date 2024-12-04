'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description:
 '''
from enum import Enum
import pygame as pg

from src.world.level import Level
from src.config import SCALING_FACTOR, GRAVITY, TILE_SIZE

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


def snap_position(
    sides: set[CornerSide],
    objects: list[ObjectCollision],
    position: pg.Vector2,
    image: pg.Surface,
    velocity: pg.Vector2
) -> None:
    """
    Snap the player position to the object it is colliding with
    """
    # pylint: disable=fixme
    # todo see how to choose the right object

    if {CornerSide.TOP_LEFT, CornerSide.BOTTOM_LEFT}.issubset(sides):
        position.x = objects[0].x + objects[0].size_x +1
        velocity.x = 0
    elif {CornerSide.TOP_RIGHT, CornerSide.BOTTOM_RIGHT}.issubset(sides):
        position.x = objects[0].x - image.get_width() * SCALING_FACTOR -1
        velocity.x = 0
    elif CornerSide.TOP_LEFT in sides or CornerSide.TOP_RIGHT in sides:
        position.y = objects[0].y + objects[0].size_y
        velocity.y = GRAVITY
    elif CornerSide.BOTTOM_LEFT in sides or CornerSide.BOTTOM_RIGHT in sides:
        position.y = objects[0].y - image.get_height() * SCALING_FACTOR
        velocity.y = 0


def handle_collision(level: Level, position: pg.Vector2, image: pg.Surface, velocity: pg.Vector2) -> None:
    """
    Handle collision with the level
    """
    player = ObjectCollision(
        position.x,
        position.y,
        int(image.get_width() * SCALING_FACTOR),
        int(image.get_height() * SCALING_FACTOR)
    ) # 100.0, 546.0 with size 32, 32

    sides_colliding: set[CornerSide] = set()
    objects_colliding = []

    exit_tile = ObjectCollision(
            level.exit_position[0] * TILE_SIZE,
            level.exit_position[1]* TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )
    if player.is_colliding(exit_tile):
        level.finished = True  

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
        snap_position(sides_colliding, objects_colliding, position, image, velocity)
        