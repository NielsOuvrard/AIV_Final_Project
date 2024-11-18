'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:40:33
 # @ Description:
 '''

from typing import Any
import toml
import pygame as pg

TILE_SIZE = 64
TOML_FILE = "assets/level.toml"

class Level:
    """
    Level class to represent the level
    """
    def __init__(self, name: str,
            layout: list[str],
            start_position: tuple[int, int],
            enemies: list[tuple[int, int]]) -> None:
        self.name: str = name
        self.layout: list[str] = layout
        self.start_position: tuple[int, int] = start_position
        self.enemies: list[tuple[int, int]] = enemies


class LevelHandler:
    """
    Level class to represent the level
    """
    def __init__(self) -> None:
        self.levels: list[Level] = []
        self.load_levels(TOML_FILE)
        self.current_level: Level = self.levels[0]

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

            layout_2d: list[str] = []
            x = 0
            width = -1
            for i, tile in enumerate(layout):
                if tile == '\n':
                    if width == -1:
                        width = i
                    layout_2d.append(str(layout[x * width + x:i]))
                    x += 1

                if tile == 'P':
                    start_position = (x, i)
                elif tile == 'E':
                    enemies.append((x, i))

            self.levels.append(Level(name, layout_2d, start_position, enemies))

    def change_level(self, level_name: str) -> None:
        for level in self.levels:
            if level.name == level_name:
                self.current_level = level
                break

    def draw(self, screen: pg.Surface) -> None:
        for i, row in enumerate(self.current_level.layout):
            for x, tile in enumerate(row):
                if tile == '#':
                    pg.draw.rect(screen, (255, 0, 0), (x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif tile == 'E':
                    pg.draw.rect(screen, (0, 0, 255), (x * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
