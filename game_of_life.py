import copy
import numpy as np
import sys
import time
from patterns import Patterns


class GameOfLife:

    def __init__(self, width=200, height=200, cell_size=20, generations=200, delay=100):
        """ Set up Conway's Game of Life. """
        # Here we create two grids to hold the old and new configurations.
        # This assumes a width x height grid of cells.
        # Each cell is either alive or dead, represented by integer values of 1 and 0, respectively.
        self.delay = delay  # interval between each "round" of the game, in ms
        self.width = width
        self.height = height
        self.old_grid = [[0] * width for _ in range(height)]
        self.new_grid = [[0] * width for _ in range(height)]
        self.generations = generations  # The maximum number of generations
        self.playing = False
        self.cell_size = cell_size
        self.t = 0  # current generation
        self.population

    @property
    def population(self):
        return sum(_.count(1) for _ in self.old_grid)

    def get_num_live_neighbors(self, x, y):
        # compute 8-neighbor sum
        # using toroidal boundary conditions - x and y wrap around
        # so that the simulation takes place on a toroidal surface.
        above = (x - 1) % self.height
        below = (x + 1) % self.height
        left = (y - 1) % self.width
        right = (y + 1) % self.width

        # Count the number of living neighbors:
        alive_neighbors = 0
        alive_neighbors += self.old_grid[above][left]  # Top-left neighbor
        alive_neighbors += self.old_grid[above][y]  # Top neighbor
        alive_neighbors += self.old_grid[above][right]  # Top-right neighbor
        alive_neighbors += self.old_grid[x][left]  # Left neighbor
        alive_neighbors += self.old_grid[x][right]  # Right neighbor
        alive_neighbors += self.old_grid[below][left]  # Bottom-left neighbor
        alive_neighbors += self.old_grid[below][y]  # Bottom neighbor
        alive_neighbors += self.old_grid[below][right]  # Bottom-right

        return alive_neighbors

    def apply_conways_rules(self):
        for x in range(self.height):
            for y in range(self.width):
                alive_neighbors = self.get_num_live_neighbors(x, y)
                if self.old_grid[x][y] == 1 and alive_neighbors < 2:
                    self.new_grid[x][y] = 0  # Dead from starvation.
                elif self.old_grid[x][y] == 1 and (alive_neighbors == 2 or alive_neighbors == 3):
                    self.new_grid[x][y] = 1  # Continue living.
                elif self.old_grid[x][y] == 1 and alive_neighbors > 3:
                    self.new_grid[x][y] = 0  # Dead from overcrowding.
                elif self.old_grid[x][y] == 0 and alive_neighbors == 3:
                    self.new_grid[x][y] = 1  # Alive from reproduction.
        # The new configuration becomes the old configuration for the next generation.
        self.old_grid = copy.deepcopy(self.new_grid)
        # Advance to next generation
        self.t += 1

    def toggle_cell_state(self, x, y):
        if not self.old_grid[x][y]:
            self.old_grid[x][y] = 1
        else:
            self.old_grid[x][y] = 0

    def reset_game(self):
        self.playing = False
        self.t = 0

    def clear_board(self):
        self.old_grid = [[0] * self.width for _ in range(self.height)]
        self.new_grid = [[0] * self.width for _ in range(self.height)]

    def add_pattern(self, pattern_name, x, y):
        """ Adds pattern to grid with top cell at (x, y) """
        pattern = Patterns.get_pattern(pattern_name)
        if pattern:
            pattern_rows = len(pattern)
            pattern_cols = len(pattern[0])
            for i in range(0, pattern_rows):
                for j in range(0, pattern_cols):
                    self.old_grid[x + i][y + j] = pattern[i][j]

    def create_random_grid(self):
        """returns a grid of width x height random values"""
        # opting for numpy here to use probability and have more dead than alive cells
        np_array = np.random.choice([1, 0], self.height * self.width, p=[0.2, 0.8]).reshape(self.height, self.width)
        self.old_grid = np_array.tolist()

    def play_with_python(self):
        # for debugging purposes
        self.add_pattern('glider', 1, 1)
        print('\n' * 5)

        while self.t < self.generations:
            print('\n' * 10)
            for row in self.old_grid:
                print(*row)
            self.apply_conways_rules()
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print("Conway's Game of Life")
            sys.exit()


if __name__ == "__main__":
    game = GameOfLife(10, 5, 5, 10)
    game.play_with_python()

