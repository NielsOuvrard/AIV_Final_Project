'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:40:33
 # @ Description:
 '''

from typing import Any
import toml
import pygame as pg
from src.config import TILE_SIZE

TOML_FILE = "assets/level.toml"


class Tile:
    """
    Tile class to represent a tile in the level
    """
    def __init__(self, x: int, y: int, size: int, color: tuple[int, int, int]) -> None:
        self.rect: pg.Rect = pg.Rect(x, y, size, size)
        self.color: tuple[int, int, int] = color

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, self.color, self.rect)

class Level:
    """
    Level class to represent the level
    """
    def __init__(self, name: str,
            tiles: list[Tile],
            start_position: tuple[int, int],
            enemies: list[tuple[int, int]]) -> None:
        self.name: str = name
        self.tiles: list[Tile] = tiles
        self.start_position: tuple[int, int] = start_position
        self.enemies: list[tuple[int, int]] = enemies
        self.tile_size = TILE_SIZE


class LevelHandler:
    """
    Level class to represent the level
    """
    def __init__(self) -> None:
        self.levels: list[Level] = []
        self.load_levels(TOML_FILE)
        self.current_level: Level = self.levels[1]

    def load_levels(self, toml_file: str) -> None:
        """
        Load levels from a toml file
        """
        with open(toml_file, 'r', encoding='utf-8') as file:
            data: dict[str, Any] = toml.load(file)

        for level_data in data['level']:
            name: str = level_data['name']
            layout: list[str] = level_data['layout']
            start_position: tuple[int, int] = (0, 0)
            enemies: list[tuple[int, int]] = []

            tiles: list[Tile] = []
            y = 0
            width = -1
            for i, tile in enumerate(layout):
                if tile == '\n':
                    if width == -1:
                        width = i
                    y += 1

                if tile == 'P':
                    start_position = ((i - y * width - y) * TILE_SIZE, y * TILE_SIZE)
                    print(f'Start position: {start_position} at level {name}, [{i - y * width - y}, {y}] {width}')
                elif tile == 'E':
                    enemies.append(((i - y * width - y) * TILE_SIZE, y * TILE_SIZE))
                elif tile == '#':
                    tiles.append(Tile((i - y * width - y) * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, (255, 0, 0)))

            self.levels.append(Level(name, tiles, start_position, enemies))

    def change_level(self, level_name: str) -> None:
        for level in self.levels:
            if level.name == level_name:
                self.current_level = level
                break

    def draw(self, screen: pg.Surface) -> None:
        for tile in self.current_level.tiles:
            tile.draw(screen)
