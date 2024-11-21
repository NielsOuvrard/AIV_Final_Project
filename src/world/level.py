'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:40:33
 # @ Description:
 '''

from math import sqrt
from typing import Any
from dataclasses import dataclass, field

import toml
import pygame as pg


from src.config import TILE_SIZE
from src.core import Graph, Node, dijkstra

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

@dataclass
class Level:
    """
    Level class to represent the level
    """
    name: str
    tiles: list[Tile]
    start_position: tuple[int, int]
    enemies: list[tuple[int, int]]
    exit_position: tuple[int, int]
    graph: Graph
    graph_result: dict[str, Node] = field(init=False)
    to_print: list[tuple[tuple[int, int], tuple[int, int]]] = field(default_factory=list)

    def __post_init__(self):
        x, y = self.start_position
        self.graph_result = dijkstra(self.graph, f'{x}-{y}')

        ex, ey = self.exit_position
        solution = self.graph_result[f'{ex}-{ey}'].path
        solution.append(f'{ex}-{ey}')

        last = self.start_position
        for path in solution:
            x, y = map(int, path.split('-'))
            self.to_print.append((last, (x, y)))
            last = (x, y)

class LevelHandler:
    """
    Level class to represent the level
    """
    def __init__(self) -> None:
        self.levels: list[Level] = []
        self.load_levels(TOML_FILE)
        self.current_level: Level = self.levels[0]
        self.world_image = pg.image.load("assets/world.png").convert_alpha()
        self.frames: dict[str, tuple[int, int]] = {}
        self.frame_dimensions: tuple[int, int]
        self.load_frames_world("assets/world.toml")


    def load_frames_world(self, toml_path: str):
        """
        Load animations from a TOML file
        """
        config = toml.load(toml_path)

        self.frame_dimensions = (config['blocks']['frame_width'], config['blocks']['frame_height'])

        for name, frame_data in config['blocks'].items():
            if name in {'frame_width', 'frame_height'}:
                continue


            x = frame_data['y_position']
            y = frame_data['x_position']
            self.frames[name] = (x, y)

    def load_levels(self, toml_file: str) -> None:
        """
        Load levels from a toml file
        """
        def get_local_x(x: int) -> int:
            return x - y * width - y

        with open(toml_file, 'r', encoding='utf-8') as file:
            data: dict[str, Any] = toml.load(file)

        for level_data in data['level']:
            start_position: tuple[int, int] = (0, 0)
            enemies: list[tuple[int, int]] = []

            tiles: list[Tile] = []
            local_graph: dict[str, dict[str, float]] = {}
            local_exit_position = (0, 0)

            y = 0
            width = -1
            for i, tile in enumerate(level_data['layout']):
                if tile == '\n':
                    if width == -1:
                        width = i
                    y += 1

                if tile == 'P':
                    start_position = (get_local_x(i), y)
                elif tile == 'E':
                    enemies.append((get_local_x(i) * TILE_SIZE, y * TILE_SIZE))
                elif tile == '#':
                    tiles.append(Tile(get_local_x(i) * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, (255, 0, 0)))
                elif tile == 'S':
                    local_exit_position = (get_local_x(i), y)

                if tile not in ['\n', '#']:
                    local_graph[f'{get_local_x(i)}-{y}'] = self.get_neighbour(level_data['layout'], i, y, width)

            self.levels.append(
                Level(level_data['name'],
                tiles,
                start_position,
                enemies,
                local_exit_position,
                Graph(local_graph))
            )

    def change_level(self, level_name: str) -> None:
        for level in self.levels:
            if level.name == level_name:
                self.current_level = level
                break

    def draw(self, screen: pg.Surface) -> None:
        """
        Draw the level
        """
        def draw_tile_here(x: int, y: int, name: str) -> None:
            brick_image = self.world_image.subsurface((*self.frames[name], *self.frame_dimensions))
            screen.blit(
                pg.transform.scale(brick_image, (TILE_SIZE, TILE_SIZE)),
                (x, y)
            )

        for tile in self.current_level.tiles:
            x, y = tile.rect.topleft
            draw_tile_here(x, y, 'brick')

        ex, ey = self.current_level.exit_position
        draw_tile_here(ex * TILE_SIZE, ey * TILE_SIZE, 'exit')

        for elem in self.current_level.to_print:
            x, y = elem[0]
            x2, y2 = elem[1]
            pg.draw.line(screen, (0, 0, 255),
                (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2),
                (x2 * TILE_SIZE + TILE_SIZE // 2, y2 * TILE_SIZE + TILE_SIZE // 2), 5)
