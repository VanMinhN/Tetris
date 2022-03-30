import random

import pygame

from pygame import mixer
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6

"""

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.font.init()
pygame.init()  # Initiate pygame

# GLOBALS VARS
s_width = 800  # screen width
s_height = 700  # screen height
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
quit_boolean = True

# Collision checking
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# Music Variable
# Sound effect -> file extension must be .wav for pygame
# Music/soundtrack -> file extension can be .wav or .mp3 for pygame

# Credit: https://mixkit.co/free-sound-effects/click/
ButtonSound = pygame.mixer.Sound("./Soundtrack/ButtonClick.wav")
ButtonSound.set_volume(0.4)
# Credit: https://archive.org/details/TetrisThemeMusic
# get the soundtrack in music folder
soundtrack = pygame.mixer.music.load("./Soundtrack/Tetris.mp3")
# -1 is to play continuously even when the sound track is end, it will replay
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


# This is S shape
#     00
#    00
# and their rotate
#    0
#    00
#     0
S = [
    [".....", "......", "..00..", ".00...", "....."],
    [".....", "..0..", "..00.", "...0.", "....."],
]

# This is Z shape
#     00
#      00
# and their rotate
#     0
#    00
#    0
Z = [
    [".....", ".....", ".00..", "..00.", "....."],
    [".....", "..0..", ".00..", ".0...", "....."],
]

# This is I shape
#     0000
# and their rotate
#     0
#     0
#     0
#     0
I = [
    ["..0..", "..0..", "..0..", "..0..", "....."],
    [".....", "0000.", ".....", ".....", "....."],
]

# This is Square shape
#     00
#     00
O = [[".....", ".....", ".00..", ".00..", "....."]]

# This is J shape and its rotation
#     0
#     000
J = [
    [".....", ".0...", ".000.", ".....", "....."],
    [".....", "..00.", "..0..", "..0..", "....."],
    [".....", ".....", ".000.", "...0.", "....."],
    [".....", "..0..", "..0..", ".00..", "....."],
]

# This is L shape and its rotation
#     0
#   000
L = [
    [".....", "...0.", ".000.", ".....", "....."],
    [".....", "..0..", "..0..", "..00.", "....."],
    [".....", ".....", ".000.", ".0...", "....."],
    [".....", ".00..", "..0..", "..0..", "....."],
]

# This is T shape and its rotation
#     000
#      0
T = [
    [".....", "..0..", ".000.", ".....", "....."],
    [".....", "..0..", "..00.", "..0..", "....."],
    [".....", ".....", ".000.", "..0..", "....."],
    [".....", "..0..", ".00..", "..0..", "....."],
]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (128, 0, 128),
]
# index 0 - 6 represent shape

# Tetris piece class


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


# Button Class


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            # pygame.mouse.get_pressed()[0] -> 0 is left mouse, 1 is middle mouse, 2 is right mouse
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


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
            if column == "0":
                pos.append((shape.x + j, shape.y + i))

    for i, index in enumerate(pos):
        pos[i] = (index[0] - 2, index[1] - 4)

    return pos


def valid_space(shape, grid):
    # Create Sublist like [[(2,3)], [(0,1)]]
    valid_pos = [
        [(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)
    ]
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


def draw_text_middle(surface, text, size, color, pos):
    font = pygame.font.SysFont("calibri", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(
        label,
        (
            top_left_x + play_width / 2 - (label.get_width() / 2),
            top_left_y + play_height / 2 - (label.get_height() / 2) + pos,
        ),
    )


def draw_grid(surface, grid):
    start_x = top_left_x
    start_y = top_left_y
    # Drawing 20 vertical lines and 10 horizontal lines
    for i in range(len(grid)):
        pygame.draw.line(
            surface,
            (128, 128, 128),
            (start_x, start_y + i * block_size),
            (start_x + play_width, start_y + i * block_size),
        )
        for j in range(len(grid[i])):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (start_x + j * block_size, start_y),
                (start_x + j * block_size, start_y + play_height),
            )


def clear_rows(grid, locked):
    inc = 0  # to keep track of many row need to shift down after del row
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    # Shift the row down after deleting row
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                # create new key at pos (x, y+inc)
                locked[newKey] = locked.pop(key)
    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("calibri", 35)
    label = font.render("Next Shape", 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height / 2 - 100

    style = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(style):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(
                    surface,
                    shape.color,
                    (
                        start_x + j * block_size,
                        start_y + i * block_size,
                        block_size,
                        block_size,
                    ),
                )
                pygame.draw.rect(
                    surface,
                    (128, 128, 128),
                    (
                        start_x + j * block_size,
                        start_y + i * block_size,
                        block_size,
                        block_size,
                    ),
                    1,
                )
    surface.blit(label, (start_x + 10, start_y - 30))


def draw_window(surface, grid, score, last_score):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont("calibri", 70)
    label = font.render("Tetris", 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width /
                 2 - (label.get_width() / 2), 30))
    # drawing the score
    font = pygame.font.SysFont("calibri", 35)
    label = font.render("Score: " + str(score), 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height / 2 - 100
    surface.blit(label, (start_x + 20, start_y + 180))

    # drawing high score
    font = pygame.font.SysFont("calibri", 30)
    label = font.render("High Score: " + str(last_score), 1, (255, 255, 255))

    start_x = top_left_x - 250
    start_y = top_left_y + 200
    surface.blit(label, (start_x + 20, start_y + 180))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (
                    top_left_x + j * block_size,
                    top_left_y + i * block_size,
                    block_size,
                    block_size,
                ),
                0,
            )

    draw_grid(surface, grid)
    pygame.draw.rect(
        surface, (255, 0, 0), (top_left_x, top_left_y,
                               play_width, play_height), 5
    )
    # pygame.display.update()


def max_score():
    with open("score.txt", "r") as f:
        lines = f.read().splitlines()  # remove newline
        score = lines
    return score


def update_score(_score):
    score = max_score()
    score2 = str(score).lstrip("['").rstrip("']")
    with open("score.txt", "w") as f:
        if int(score2) > _score:  # convert string into int for comparing
            f.write(str(score))
        else:
            f.write(str(_score))


def main(win):
    global quit_boolean
    # remove [' and '] in the list
    last_score = str(max_score()).lstrip("['").rstrip("']")
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
    level_time = 0
    score = 0
    # game loop
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if (level_time / 1000) > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_boolean = False
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # move block left
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:  # move block right
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:  # rotate key
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:  # drop the block down faster
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
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
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "You Lost!", 90, (255, 255, 255), 0)
            pygame.display.update()
            pygame.time.delay(1500)  # delay for one and half a second
            run = False
            update_score(score)


def main_menu(win):
    global quit_boolean
    # create button instance
    start_btn = Button(s_width/2 - 100, s_height/2, start_btn_image, 0.2)
    rule_btn = Button(s_width/2 - 100, s_height/2 + 100, rule_btn_image, 1)
    exit_btn = Button(s_width/2 - 100, s_height/2 + 200, exit_btn_image, 0.2)
    run = True
    while run:
        win.fill((0, 0, 0))  # fill the screen with black
        # draw_text_middle(win, "Press Any key to Play", 60, (255, 255, 255))
        if start_btn.draw(win):
            ButtonSound.play()
            main(win)
        # Rules Option in the Main Menu
        if rule_btn.draw(win):
            ButtonSound.play()
            rules_window(win)
        # Exit Btn
        if exit_btn.draw(win):
            ButtonSound.play()
            run = False
        pygame.display.update()
        for event in pygame.event.get():  # event game handler
            if event.type == pygame.QUIT:  # quit game
                run = False
        if not quit_boolean:
            run = False
    pygame.display.quit()  # quit the window


# Will Create a New window for Game rules and such


def rules_window(win):
    run = True
    global quit_boolean
    # Game Loop
    while run:
        win.fill((0, 0, 0))  # Fill the screen with black color
        # Draw the Rules/Instructions in the window
        # First line will be key control -> Num.Key left and right, up is rotation, down is speed up the fall
        draw_text_middle(
            win, "Movement: Use Arrow Keys to control the Tetris pieces", 20, (255, 255, 255), -200)
        draw_text_middle(
            win, "Arrow Key Up is rotating the piece, Arrow Key down is speed up fallen speed", 20, (255, 255, 255), -150)
        draw_text_middle(
            win, "Arrow Key Left is to move piece to the left, Arrow Key right is move to the right", 20, (255, 255, 255), -100)
        draw_text_middle(
            win, "Scoring: Any fill row is worth 10 points", 20, (255, 255, 255), 0)
        draw_text_middle(
            win, "Press any key to go back after finish reading the instruction", 20, (255, 255, 255), 150)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit_boolean = False
            if event.type == pygame.KEYDOWN:
                run = False
    pygame.display.update()  # Testing


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")

# Load Button Img
# Source: Menu vector created by upklyak - https://www.freepik.com/free-vector/set-game-menu-elements-textile-woven-texture-icons_24655610.htm#query=exit%20button&position=1&from_view=search
start_btn_image = pygame.image.load("./img/Start_BTN.jpg").convert_alpha()

# Exit Button Img
# Source: Menu vector created by upklyak - https://www.freepik.com/free-vector/set-game-menu-elements-textile-woven-texture-icons_24655610.htm#query=exit%20button&position=1&from_view=search
exit_btn_image = pygame.image.load("./img/Exit_BTN.jpg").convert_alpha()

# Help/Rules Button Img
# Source: GUI Items created by GameSupplyGuy - https://gamesupply.itch.io/gui-items-buttons
rule_btn_image = pygame.image.load("./img/Rules_BTN.png").convert_alpha()

main_menu(win)  # start game
