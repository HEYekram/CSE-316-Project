import pygame
import sys
import math
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

# Configuration
INITIAL_WINDOW_SIZE = 800
MIN_WINDOW_SIZE = 400
GRID_SIZE = 50
HEURISTIC = "manhattan"  # Options: "manhattan", "euclidean", "chebyshev"
DIAGONAL_MOVEMENT = False
COLORS = {
    "background": (255, 255, 255),
    "grid": (200, 200, 200),
    "start": (255, 165, 0),
    "end": (64, 224, 208),
    "barrier": (0, 0, 0),
    "open": (0, 255, 0),
    "closed": (255, 0, 0),
    "path": (128, 0, 128),
    "text": (0, 0, 0)
}

class PathfindingVisualizer:
    def __init__(self):
        self.window_size = INITIAL_WINDOW_SIZE
        self.node_size = self.window_size // GRID_SIZE  # Calculate first
        self.window = pygame.display.set_mode(
            (self.window_size, self.window_size), pygame.RESIZABLE)
        pygame.display.set_caption("Resizable A* Pathfinder")
        self.grid = self.create_grid()  # Now this can use self.node_size
        self.start = None
        self.end = None
        self.stats = {"visited": 0, "path_length": 0, "time": 0}
        
    class Node:
        def __init__(self, row, col, node_size):
            self.row = row
            self.col = col
            self.node_size = node_size
            self.x = row * node_size
            self.y = col * node_size
            self.color = COLORS["background"]
            self.neighbors = []
            self.weight = 1

        def get_pos(self):
            return (self.row, self.col)

        def update_size(self, new_size):
            self.node_size = new_size
            self.x = self.row * new_size
            self.y = self.col * new_size

        def draw(self, surface):
            pygame.draw.rect(surface, self.color, 
                            (self.x, self.y, self.node_size, self.node_size))

        def update_neighbors(self, grid):
            self.neighbors = []
            directions = [
                (1, 0), (-1, 0), (0, 1), (0, -1)
            ]
            if DIAGONAL_MOVEMENT:
                directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

            for dr, dc in directions:
                r = self.row + dr
                c = self.col + dc
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    if not grid[r][c].is_barrier():
                        self.neighbors.append(grid[r][c])

        def is_barrier(self):
            return self.color == COLORS["barrier"]

        def reset(self):
            self.color = COLORS["background"]
            self.weight = 1

    def create_grid(self):
        return [[self.Node(i, j, self.node_size) for j in range(GRID_SIZE)] 
                for i in range(GRID_SIZE)]

    def handle_resize(self, new_size):
        new_size = max(new_size, MIN_WINDOW_SIZE)
        self.window_size = new_size
        self.node_size = self.window_size // GRID_SIZE
        self.window = pygame.display.set_mode(
            (self.window_size, self.window_size), pygame.RESIZABLE)
        
        # Update all nodes with new sizes
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.grid[i][j].update_size(self.node_size)

    def draw_grid(self):
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(self.window, COLORS["grid"],
                           (0, i * self.node_size), 
                           (self.window_size, i * self.node_size))
            pygame.draw.line(self.window, COLORS["grid"],
                           (i * self.node_size, 0), 
                           (i * self.node_size, self.window_size))

    def draw_interface(self):
        font = pygame.font.Font(None, 24)
        text = [
            "LMB: Place Start/End/Barriers",
            "RMB: Remove Nodes",
            "SPACE: Start Search",
            "C: Clear Grid",
            f"Window Size: {self.window_size}px",
            f"Node Size: {self.node_size}px",
            f"Heuristic: {HEURISTIC.capitalize()}",
            f"Diagonal: {DIAGONAL_MOVEMENT}"
        ]
        y_offset = 10
        for line in text:
            text_surf = font.render(line, True, COLORS["text"])
            self.window.blit(text_surf, (10, y_offset))
            y_offset += 25

    def heuristic(self, a, b):
        x1, y1 = a
        x2, y2 = b
        if HEURISTIC == "manhattan":
            return abs(x1 - x2) + abs(y1 - y2)
        elif HEURISTIC == "euclidean":
            return math.hypot(x1 - x2, y1 - y2)
        elif HEURISTIC == "chebyshev":
            return max(abs(x1 - x2), abs(y1 - y2))
        return 0

    def reconstruct_path(self, came_from, current):
        while current in came_from:
            current = came_from[current]
            if current != self.start:
                current.color = COLORS["path"]
                self.stats["path_length"] += 1
        self.end.color = COLORS["end"]

    def a_star(self):
        open_set = PriorityQueue()
        open_set.put((0, 0, self.start))
        came_from = {}
        g_score = {node: float("inf") for row in self.grid for node in row}
        g_score[self.start] = 0
        f_score = {node: float("inf") for row in self.grid for node in row}
        f_score[self.start] = self.heuristic(self.start.get_pos(), 
                                           self.end.get_pos())

        open_set_hash = {self.start}
        self.stats = {"visited": 0, "path_length": 0, "time": 0}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == self.end:
                self.reconstruct_path(came_from, current)
                return True

            for neighbor in current.neighbors:
                temp_g = g_score[current] + current.weight

                if temp_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g
                    f_score[neighbor] = temp_g + self.heuristic(
                        neighbor.get_pos(), self.end.get_pos())
                    if neighbor not in open_set_hash:
                        open_set.put((f_score[neighbor], id(neighbor), neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.color = COLORS["open"]

            self.stats["visited"] += 1
            self.draw()
            
            if current != self.start:
                current.color = COLORS["closed"]

        return False

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[0] // self.node_size
        col = mouse_pos[1] // self.node_size
        
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            if pygame.mouse.get_pressed()[0]:  # Left mouse
                node = self.grid[row][col]
                if not self.start and node != self.end:
                    self.start = node
                    node.color = COLORS["start"]
                elif not self.end and node != self.start:
                    self.end = node
                    node.color = COLORS["end"]
                elif node != self.start and node != self.end:
                    node.color = COLORS["barrier"]

            if pygame.mouse.get_pressed()[2]:  # Right mouse
                node = self.grid[row][col]
                node.reset()
                if node == self.start:
                    self.start = None
                elif node == self.end:
                    self.end = None

    def draw(self):
        self.window.fill(COLORS["background"])
        for row in self.grid:
            for node in row:
                node.draw(self.window)
        self.draw_grid()
        self.draw_interface()
        pygame.display.update()

    def reset_grid(self):
        self.start = None
        self.end = None
        self.grid = self.create_grid()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.handle_resize(min(event.w, event.h))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.start and self.end:
                        for row in self.grid:
                            for node in row:
                                node.update_neighbors(self.grid)
                        self.a_star()
                    if event.key == pygame.K_c:
                        self.reset_grid()
                    if event.key == pygame.K_d:
                        global DIAGONAL_MOVEMENT
                        DIAGONAL_MOVEMENT = not DIAGONAL_MOVEMENT
                    if event.key == pygame.K_h:
                        global HEURISTIC
                        heuristics = ["manhattan", "euclidean", "chebyshev"]
                        HEURISTIC = heuristics[
                            (heuristics.index(HEURISTIC) + 1) % len(heuristics)]

            self.handle_input()
            self.draw()

if __name__ == "__main__":
    visualizer = PathfindingVisualizer()
    visualizer.run()