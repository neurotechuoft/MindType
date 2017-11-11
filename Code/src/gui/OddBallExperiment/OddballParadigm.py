"""
Simple binary oddball paradigm

Pratham Desai
"""
import sys
import pygame

RED = (255, 0, 0)
BLUE = (0, 0, 255)
surface_width = 500
surface_height = 500
delta = 1000


def game():
    pygame.init()

    surface = pygame.display.set_mode((surface_width, surface_height))

    current_time = pygame.time.get_ticks()

    interval = current_time + delta
    show = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = pygame.time.get_ticks()

        if current_time >= interval:
            interval = current_time + delta
            show = not show

        surface.fill(RED)

        if show:
            pygame.draw.rect(surface, BLUE, (0, 0, surface_width, surface_height))

        pygame.display.update()


if __name__ == '__main__':
    game()
