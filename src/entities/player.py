'''
 # @ Author: Niels Ouvrard - Diego Jiménez Ontiveros - Santiago Arreola Munguia
 # @ Create Time: 2024-11-12 19:39:56
 # @ Description:
 '''

import pygame
import toml
from src.config import SCALING_FACTOR, SCREEN_HEIGHT, GRAVITY

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.sprite_sheet = pygame.image.load("assets/mario_bros.png").convert_alpha()
        self.animations = {}
        self.current_animation = 'idle'
        self.animation_speed = 0.1
        self.animation_time = 0
        self.frame_index = 0
        self.load_animations()

        # debug
        self.ground_y = SCREEN_HEIGHT - (SCREEN_HEIGHT // 3)

        self.position = pygame.Vector2(100, self.ground_y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        
    def get_frame(self, sprite_sheet: pygame.Surface, x: int, y: int, width: int, height: int) -> pygame.Surface:
        frame = pygame.Surface((width, height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (x, y, width, height))
        return frame

    def load_animations(self):
        config = toml.load('assets/mario_bros.toml')
        frame_width = config['animations']['frame_width']
        frame_height = config['animations']['frame_height']

        for animation_name, animation_data in config['animations'].items():
            if animation_name == 'frame_width' or animation_name == 'frame_height':
                continue

            frame_count = animation_data['frame_count']
            y_position = animation_data['y_position']
            x_positions = animation_data['x_positions']

            frames = []
            for x in x_positions:
                frame = self.get_frame(self.sprite_sheet, x, y_position, frame_width, frame_height)
                frames.append(frame)
            self.animations[animation_name] = frames
            

    def move_and_slide(self):
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

    def animate(self, dt: float):
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

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.change_animation('jump')
                self.acceleration.y = -5
            if event.key == pygame.K_RIGHT:
                self.change_animation('walk')
                self.acceleration.x = 0.1
            if event.key == pygame.K_LEFT:
                self.change_animation('walk')
                self.acceleration.x = -0.1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                self.acceleration.x = 0

    def draw(self, screen: pygame.Surface):
        if self.velocity.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.transform.flip(self.image, False, False)
        screen.blit(pygame.transform.scale(self.image,
                                          (self.image.get_width() * SCALING_FACTOR, self.image.get_height() * SCALING_FACTOR)),
                   (self.position.x, self.position.y))