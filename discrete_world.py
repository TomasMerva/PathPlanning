import pygame, pygame_gui
from colors import Colors


class Node:
    def __init__(self, index_row, index_col, grid_size, total_rows):
        # Discrete position
        self.index_row = index_row
        self.index_col = index_col
        # Continous position that is required for pygame
        self.position_x = 640+ index_col * grid_size[1]
        self.position_y = index_row * grid_size[0]
        self.grid_size = grid_size
        self.neighbors = []
        self.total_rows = total_rows

        # For Djikstra
        self.cost = 1

        # Graphics properties
        self.colors_list = Colors()
        self.color = self.colors_list.WHITE


    def get_index_pos(self):
        return self.index_row, self.index_col

    def reset(self):
        self.color = self.colors_list.WHITE

    def is_dead(self):
        return self.color == self.colors_list.SLATEGREY

    def is_alive(self):
        return self.color == self.colors_list.GREEN

    def is_obstacle(self):
        return self.color == self.colors_list.BLACK

    def make_dead(self):
        self.color = self.colors_list.SLATEGREY

    def make_alive(self):
        self.color = self.colors_list.GREEN

    def make_obstacle(self):
        self.color = self.colors_list.BLACK

    def make_path(self):
        self.color = self.colors_list.PURPLE

    def make_start(self):
        self.color = self.colors_list.YELLOW

    def make_goal(self):
        self.color = self.colors_list.ORANGE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.position_x, self.position_y, self.grid_size[0], self.grid_size[1]))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Neighbor on right
        if self.index_col < self.total_rows-1 and not grid[self.index_row][self.index_col + 1].is_obstacle():
            self.neighbors.append(grid[self.index_row][self.index_col + 1])
        # Neighbor on left
        if self.index_col > 0 and not grid[self.index_row][self.index_col - 1].is_obstacle():
            self.neighbors.append(grid[self.index_row][self.index_col - 1])
        # Neighbor up
        if self.index_row > 0 and not grid[self.index_row-1][self.index_col].is_obstacle():
            self.neighbors.append(grid[self.index_row-1][self.index_col])
        # Neighbor down
        if self.index_row < self.total_rows-1 and not grid[self.index_row + 1][self.index_col].is_obstacle():
            self.neighbors.append(grid[self.index_row+1][self.index_col])
        # Top-right corner
        if self.index_row > 0 and self.index_col < self.total_rows-1 and not grid[self.index_row-1][self.index_col+1].is_obstacle():
            self.neighbors.append(grid[self.index_row-1][self.index_col+1])
        # Top-left corner
        if self.index_row > 0 and self.index_col > 0 and not grid[self.index_row-1][self.index_col-1].is_obstacle():
            self.neighbors.append(grid[self.index_row-1][self.index_col-1])
        # Bottom-right corner
        if self.index_row < self.total_rows-1 and self.index_col < self.total_rows-1 and not grid[self.index_row+1][self.index_col+1].is_obstacle():
            self.neighbors.append(grid[self.index_row+1][self.index_col+1])
        # Bottom-left corner
        if self.index_row < self.total_rows-1 and self.index_col > 0 and not grid[self.index_row+1][self.index_col-1].is_obstacle():
            self.neighbors.append(grid[self.index_row+1][self.index_col-1])

    def __lt__(self, other):
        return False


class DiscreteWorld:
    def __init__(self, width, height, gui_scale=0.4, rows=10):
        self.WIDTH = width
        self.HEIGHT = height
        self.GUI_SCALE = gui_scale
        self.ROWS = rows
        self.colors_list = Colors()

        # Grid [rows,columns]
        self.GRID_SIZE = [self.HEIGHT // self.ROWS,
                          int((1-self.GUI_SCALE)*self.WIDTH) // self.ROWS]
        print("GridSize ", self.GRID_SIZE)
        self.grid = []

        # States
        self.start_node = None
        self.goal_node = None


    def make_grid(self, obstacles=False):
        self.grid = []
        # 2D list representing grid with dimension ROWS * ROWS
        for row in range(self.ROWS):
            self.grid.append([])     # append a new row
            for col in range(self.ROWS):
                # Create new node at grid[row][col]
                node = Node(index_row=row,
                            index_col=col,
                            grid_size=self.GRID_SIZE,
                            total_rows=self.ROWS)
                self.grid[row].append(node)

    def get_mouse_clicked_node(self):
        x, y = pygame.mouse.get_pos()
        if x >= self.GUI_SCALE*self.WIDTH:
            row = y // self.GRID_SIZE[0]
            col = int(x-self.GUI_SCALE*self.WIDTH) // self.GRID_SIZE[1]
            node = self.grid[row][col]
            return node
        return None
    
    def update_neighbors(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)

    def draw(self, window):
        window.fill(self.colors_list.WHITE)    # Reset pygame window
        # Draw nodes
        for row in self.grid:
            for node in row:
                node.draw(window)
        # Draw grid lines
            for i in range(self.ROWS):    
                # draw horizontal lines
                pygame.draw.line(window, self.colors_list.GREY, (self.GUI_SCALE*self.WIDTH, i * self.GRID_SIZE[0]), 
                                                                     (self.WIDTH, i * self.GRID_SIZE[0]))
                # draw vertical lines
                pygame.draw.line(window, self.colors_list.GREY, (i * self.GRID_SIZE[1] + self.GUI_SCALE*self.WIDTH, 0),            
                                                         (i * self.GRID_SIZE[1] + self.GUI_SCALE*self.WIDTH, self.HEIGHT))                
            