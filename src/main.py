import pygame


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Hello World!')

    # Set up font
    font = pygame.font.Font(None, 74)
    text = font.render('works', True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 300))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the text
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

    pygame.quit()