import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 800  # screen width
s_height = 700  # screen height
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

# Collision checking
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6

"""

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]


shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    # Init grid -> create 20 sublists with 10 list of color
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    pos = []
    style = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(style):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pos.append((shape.x + j, shape.y + i))

    for i, index in enumerate(pos):
        pos[i] = (index[0]-2, index[1] - 4)

    return pos


def valid_space(shape, grid):
    # Create Sublist like [[(2,3)], [(0,1)]]
    valid_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)]
                 for i in range(20)]
    # Convert the list above to remove the embedded list. Ex: [(2,3), (0,1)]
    valid_pos = [j for sub in valid_pos for j in sub]

    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in valid_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
# need to create new shape for the next move


def get_shape():
    global shapes, shape_colors
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, grid):
    start_x = top_left_x
    start_y = top_left_y
    # Drawing 20 vertical lines and 10 horizontal lines
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (start_x, start_y +
                         i*block_size), (start_x + play_width, start_y + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (start_x+j*block_size,
                             start_y), (start_x + j * block_size, start_y + play_height))


def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('calibri', 35)
    label = font.render('Next Shape', 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height/2 - 100

    style = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(style):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (start_x+j*block_size,
                                start_y+i*block_size, block_size, block_size))
                pygame.draw.rect(surface, (128, 128, 128), (start_x+j*block_size,
                                start_y+i*block_size, block_size, block_size), 1)
    surface.blit(label, (start_x+10, start_y-30))


def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('calibri', 70)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width /
                 2 - (label.get_width()/2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x,
                     top_left_y, play_width, play_height), 5)
    # pygame.display.update()


def main(win):
    global grid
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.28
    # game loop
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # move block left
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:  # move block right
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_UP:  # rotate key
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_DOWN:  # drop the block down faster
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

        draw_window(win, grid)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    pygame.display.quit()  # quit the game


def main_menu(win):
    main(win)


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
