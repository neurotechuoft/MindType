"""
Simple binary oddball paradigm

Pratham Desai
"""
import pygame
from random import randint
import sys

def binary_experiment(delay_time=100):

    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    surface_width = 500 + 30
    surface_height = 500 + 30

    num_rows = 5
    num_cols = 5
    grid_margin = 5
    grid_width = 100
    grid_height = 100

    # binary grid set to white
    grid = [[0 for _ in range(num_rows)] for _ in range(num_cols)]
    times = [0.0]
    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((surface_width, surface_height))

    while True:

        pygame.time.delay(60)

        random_row = randint(0, 4)
        random_col = randint(0, 4)

        if random_row == 2 and random_col == 2:

            # blue square
            grid[random_row][random_col] = 2
            times.append(clock.tick() + times[-1])
            sys.stdout = open("test-test-test.txt", "w")
            print(times)


        else:

            # red square
            grid[random_row][random_col] = 1

        # refresh color for update
        color = None

        # loop through grid and assign colors based on values
        for row in range(num_rows):
            for col in range(num_cols):

                if grid[row][col] == 1:

                    color = RED

                elif grid[row][col] == 2:

                    color = BLUE

                elif grid[row][col] == 0:

                    color = WHITE

                pygame.draw.rect(surface, color,
                                 [
                                     (grid_margin + grid_width) * col + grid_margin,
                                     (grid_margin + grid_height) * row + grid_margin,
                                     grid_width,
                                     grid_height
                                 ]
                                 )

        # wait time to refresh grid
        pygame.time.delay(delay_time)

        # reset grid
        grid = [[0 for _ in range(num_rows)] for _ in range(num_cols)]

        # update
        pygame.display.flip()

if __name__ == '__main__':

    binary_experiment()


