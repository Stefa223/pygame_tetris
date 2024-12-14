import pygame
import random


pygame.init()


WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 128, 128),
]


SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  
    [[1, 1, 1, 1]],           
    [[1, 1], [1, 1]],         
    [[0, 1, 1], [1, 1, 0]],   
    [[1, 1, 0], [0, 1, 1]],   
    [[1, 1, 1], [1, 0, 0]],   
    [[1, 1, 1], [0, 0, 1]],   
]


grid = [[0 for _ in range(WIDTH // BLOCK_SIZE)] for _ in range(HEIGHT // BLOCK_SIZE)]

def draw_grid(surface):
    for y in range(HEIGHT // BLOCK_SIZE):
        for x in range(WIDTH // BLOCK_SIZE):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)

def draw_grid_blocks(surface):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != 0:
                color = COLORS[grid[y][x] - 1]
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, WHITE, rect, 1)

class Tetrimino:
    def __init__(self, excluded_shapes=None):
        if excluded_shapes is None:
            excluded_shapes = []

        # Exclude the previous shape from the pool of possible shapes
        available_shapes = [shape for shape in SHAPES if shape not in excluded_shapes]
        self.shape = random.choice(available_shapes)
        self.color = random.randint(1, len(COLORS))
        self.x = WIDTH // BLOCK_SIZE // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def valid_move(self, dx, dy, new_shape=None):
        new_shape = new_shape or self.shape
        for y, row in enumerate(new_shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= WIDTH // BLOCK_SIZE or new_y >= HEIGHT // BLOCK_SIZE or grid[new_y][new_x]:
                        return False
        return True

    def place(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color

def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = len(grid) - len(new_grid)
    for _ in range(lines_cleared):
        new_grid.insert(0, [0 for _ in range(WIDTH // BLOCK_SIZE)])
    grid = new_grid
    return lines_cleared


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
previous_shapes = []  
current_piece = Tetrimino(previous_shapes)
previous_shapes.append(current_piece.shape)  
next_piece = Tetrimino(previous_shapes)  
fall_time = 0
fall_speed = 1000  
score = 0

while running:
    screen.fill(BLACK)
    draw_grid(screen)
    draw_grid_blocks(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_piece.valid_move(-1, 0):
                current_piece.x -= 1
            if event.key == pygame.K_RIGHT and current_piece.valid_move(1, 0):
                current_piece.x += 1
            if event.key == pygame.K_DOWN and current_piece.valid_move(0, 1):
                current_piece.y += 1
            if event.key == pygame.K_UP:
                rotated_shape = [list(row) for row in zip(*current_piece.shape[::-1])]
                if current_piece.valid_move(0, 0, rotated_shape):
                    current_piece.rotate()

    
    fall_time += clock.get_rawtime()
    clock.tick()
    if fall_time > fall_speed:
        if current_piece.valid_move(0, 1):
            current_piece.y += 1
        else:
            current_piece.place()
            lines_cleared = clear_lines()
            previous_shapes.append(current_piece.shape)  
            if len(previous_shapes) > 3:  
                previous_shapes.pop(0)
            current_piece = next_piece
            next_piece = Tetrimino(previous_shapes)  
            if not current_piece.valid_move(0, 0):
                running = False  
        fall_time = 0

    
    for y, row in enumerate(current_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (current_piece.x + x) * BLOCK_SIZE,
                    (current_piece.y + y) * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
                pygame.draw.rect(screen, COLORS[current_piece.color - 1], rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

    pygame.display.flip()

pygame.quit()
