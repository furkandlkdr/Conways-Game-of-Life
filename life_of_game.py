import time
import numpy as np
import pygame

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)

def update(screen, cells, size, with_progress=False):
    # Make a copy of the cells to update
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]), dtype=bool)

    for row, col in np.ndindex(cells.shape):
        # Count the number of neighbors that are alive
        neighbors = np.sum(cells[max(0, row-1):min(cells.shape[0], row+2), max(0, col-1):min(cells.shape[1], col+2)]) - cells[row, col]
        # Assign color that will be used to draw the cell
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        # If the cell is alive, it remains alive only if it has 2 or 3 neighbors
        if cells[row, col]:
            updated_cells[row, col] = neighbors == 2 or neighbors == 3
            if with_progress:
                color = COLOR_ALIVE_NEXT if updated_cells[row, col] else COLOR_DIE_NEXT
        # If the cell is dead, it becomes alive only if it has 3 neighbors
        else:
            updated_cells[row, col] = neighbors == 3
            if with_progress:
                color = COLOR_ALIVE_NEXT if updated_cells[row, col] else COLOR_BG

        # Draw the cell
        pygame.draw.rect(screen, color, (col*size, row*size, size - 1, size - 1))

    return updated_cells
def main():
    # Initialize the pygame
    pygame.init()
    screen = pygame.display.set_mode((800,600))

    # Create the grid
    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    # Main loop
    running = False
    while True:
        for event in pygame.event.get():
            # Quit the game if the user closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            # Pause the game if the user presses the space bar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            # Draw a cell if the user clicks on the grid
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                cells[y // 10, x // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()
        # Clear the screen
        screen.fill(COLOR_GRID)
        # Update the cells
        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)

if __name__ == "__main__":
    main();
