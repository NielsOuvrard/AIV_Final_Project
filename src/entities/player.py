'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description:
 '''

import pygame as pg
import toml
from src.config import SCALING_FACTOR, SCREEN_HEIGHT, GRAVITY
from src.world.level import Level

class Player(pg.sprite.Sprite):
    """
    Player class to represent the player character
    """
    def __init__(self):
        super().__init__()

        self.sprite_sheet = pg.image.load("assets/mario_bros.png").convert_alpha()
        self.animations = {}
        self.current_animation = 'idle'
        self.animation_speed = 0.1
        self.animation_time = 0
        self.frame_index = 0
        self.load_animations()

        # debug
        self.ground_y = SCREEN_HEIGHT - (SCREEN_HEIGHT // 11)
        self.in_ground = False

        self.position = pg.Vector2(100, self.ground_y)
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

        # Check for ground collision
        if self.position.y > self.ground_y:
            self.position.y = self.ground_y
            self.velocity.y = 0
            self.change_animation('idle' if self.velocity.x == 0 else 'walk')

        # Check for idle state
        if self.velocity.x < 0.01 and self.velocity.x > -0.01:
            self.change_animation('idle')
            self.velocity.x = 0

        x1y1 = self.position
        x2y1 = pg.Vector2(self.position.x + self.image.get_width()*SCALING_FACTOR ,self.position.y)
        x1y2 = pg.Vector2(self.position.x, self.position.y + self.image.get_height()*SCALING_FACTOR)
        x2y2 = pg.Vector2(self.position.x + self.image.get_width()*SCALING_FACTOR, self.position.y + self.image.get_height()*SCALING_FACTOR)

        tile_size = level.tile_size

        up1, up2, ri1, ri2, dw1, dw2, le1, le2 = [False]*8
        x_snap = 0
        y_snap = 0
        for i, row in enumerate(level.layout):
            for x, tile in enumerate(row):
                if tile == '#':
                    if (x1y1.x > x*tile_size and x1y1.x < (x*tile_size+tile_size) and x1y1.y > i*tile_size and x1y1.y < (i*tile_size+tile_size)):
                        up1 = True
                        le1 = True
                        x_snap = x
                        y_snap = i
                    if (x2y1.x > x*tile_size and x2y1.x < (x*tile_size+tile_size) and x2y1.y > i*tile_size and x2y1.y < (i*tile_size+tile_size)):
                        up2 = True
                        ri1 = True
                        x_snap = x
                        y_snap = i
                    if (x1y2.x > x*tile_size and x1y2.x < (x*tile_size+tile_size) and x1y2.y > i*tile_size and x1y2.y < (i*tile_size+tile_size)):
                        dw1 = True
                        le2 = True
                        x_snap = x
                        y_snap = i
                    if (x2y2.x > x*tile_size and x2y2.x < (x*tile_size+tile_size) and x2y2.y > i*tile_size and x2y2.y < (i*tile_size+tile_size)):
                        dw2 = True
                        ri2 = True
                        x_snap = x
                        y_snap = i
        if ri1 and ri2:
            self.position = pg.Vector2(x_snap*tile_size-self.image.get_width()*SCALING_FACTOR, self.position.y)
            self.acceleration.x = 0
            print("right")
        elif le1 and le2:
            self.position = pg.Vector2(x_snap*tile_size, self.position.y)
            self.acceleration.x = 0
            print("left")
        elif up1 or up2:
            self.position = pg.Vector2(self.position.x , y_snap*tile_size+tile_size)
            self.acceleration.y = 0
            print("up")
        elif (dw1 or dw2): 
            self.position = pg.Vector2(self.position.x , y_snap*tile_size-self.image.get_height()*SCALING_FACTOR)
            self.acceleration.y = 0
            self.in_ground = True
            self.velocity.y = 0
            # print("down")
        



                    # #collision with ceiling
                    # if (x1y1.x > x*tile_size and x1y1.x < (x*tile_size+tile_size) and x1y1.y > i*tile_size and x1y1.y < (i*tile_size+tile_size)) and (x2y1.x > x*tile_size and x2y1.x < (x*tile_size+tile_size) and x2y1.y > i*tile_size and x2y1.y < (i*tile_size+tile_size)):
                    #     self.position = pg.Vector2(self.position.x , i*tile_size+tile_size)
                    #     self.acceleration.y = 0
                    #     print("up")
                    # #collision with right wall
                    # if (x2y1.x > x*tile_size and x2y1.x < (x*tile_size+tile_size) and x2y1.y > i*tile_size and x2y1.y < (i*tile_size+tile_size)) and (x2y2.x > x*tile_size and x2y2.x < (x*tile_size+tile_size) and x2y2.y > i*tile_size and x2y2.y < (i*tile_size+tile_size)):
                    #     self.position = pg.Vector2(x*tile_size-self.image.get_width()*SCALING_FACTOR, self.position.y)
                    #     self.acceleration.x = 0
                    #     print("right")
                    # #collision with floor
                    # if (x1y2.x > x*tile_size and x1y2.x < (x*tile_size+tile_size) and x1y2.y > i*tile_size and x1y2.y < (i*tile_size+tile_size)) and (x2y2.x > x*tile_size and x2y2.x < (x*tile_size+tile_size) and x2y2.y > i*tile_size and x2y2.y < (i*tile_size+tile_size)):
                    #     self.position = pg.Vector2(self.position.x , i*tile_size-self.image.get_height()*SCALING_FACTOR)
                    #     self.acceleration.y = 0
                    #     self.in_ground = True
                    #     self.velocity.y = 0
                    #     print("down")
                    # #collision with left wall
                    # if (x1y1.x > x*tile_size and x1y1.x < (x*tile_size+tile_size) and x1y1.y > i*tile_size and x1y1.y < (i*tile_size+tile_size)) and (x1y2.x > x*tile_size and x1y2.x < (x*tile_size+tile_size) and x1y2.y > i*tile_size and x1y2.y < (i*tile_size+tile_size)):
                    #     self.position = pg.Vector2(x*tile_size+tile_size, self.position.y)
                    #     self.acceleration.x = 0
                    #     print("left")


                   


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
                self.acceleration.x = 0.02
            if event.key == pg.K_LEFT:
                self.change_animation('walk')
                self.acceleration.x = -0.02
        if event.type == pg.KEYUP:
            if event.key in {pg.K_RIGHT, pg.K_LEFT}:
                self.acceleration.x = 0
        # if event.type == pg.KEYUP:
        #     if event.key in {pg.K_DOWN, pg.K_SPACE}:
        #         self.acceleration.y = 0

    def draw(self, screen: pg.Surface):
        if self.velocity.x < 0:
            self.image = pg.transform.flip(self.image, True, False)
        else:
            self.image = pg.transform.flip(self.image, False, False)
        screen.blit(pg.transform.scale(self.image,
                                          (self.image.get_width() * SCALING_FACTOR,
                                           self.image.get_height() * SCALING_FACTOR)),
                   (self.position.x, self.position.y))
