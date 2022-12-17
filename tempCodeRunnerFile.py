from random import randint
import tetris
import time
game = tetris.BaseGame()
board = game.get_playfield().tolist()

# 0: empty
# 1: line
# 2: j
# 3: l
# 4: o
# 5: s
# 6: t
# 7: z
# 8: ghost

colorDict = {0: (255, 255, 255), 1: (0, 255, 255), 2: (0, 0, 255), 3: (255, 170, 0), 4: (255, 255, 0), 5: (0, 255, 0),
             6: (153, 0, 255), 7: (255, 0, 0), 8: (210, 210, 210)}

pieceGrid = {
    None: [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
    1: [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1]],
    2: [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 2, 2, 2]],
    3: [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 3, 0],
        [3, 3, 3, 0]],
    4: [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 4, 4, 0],
        [0, 4, 4, 0]],
    5: [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 5, 5],
        [0, 5, 5, 0]],
    6: [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 6, 0],
        [0, 6, 6, 6]],
    7: [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [7, 7, 0, 0],
        [0, 7, 7, 0]],
}

def pieceToNum(piece):
    if piece == tetris.PieceType.I:
        return 1
    if piece == tetris.PieceType.J:
        return 2
    if piece == tetris.PieceType.L:
        return 3
    if piece == tetris.PieceType.O:
        return 4
    if piece == tetris.PieceType.S:
        return 5
    if piece == tetris.PieceType.T:
        return 6
    if piece == tetris.PieceType.Z:
        return 7
    if piece == None:
        return None
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([s_width, s_height])

# Run until the user asks to quit
running = True

def draw_piece(surface, piece, topLeftX, topLeftY, width, length):
    topLeftX += 5
    topLeftY += 5
    width -= 5
    length -= 5
    piece_width = width//4
    piece_height = length//4
    pGrid = pieceGrid[piece]
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(surface, colorDict[pGrid[i][j]], (topLeftX + j * piece_width, topLeftY + i * piece_height, piece_width, piece_height), 0)

def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (180, 180, 180), (sx, sy + i * 30),
                         (sx + play_width - 1, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (180, 180, 180), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height - 1))  # vertical lines
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == (255, 255, 255):
                continue
            pygame.draw.rect(surface, grid[i][j], (sx + j * 30, sy + i * 30, 30, 30), 0)
lasttime = 0
interval = 50
interval_init = 170
pygame.font.init()
my_font = pygame.font.SysFont("Comic Sans", 24)
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.hard_drop()
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_z:
                game.rotate(-1)
            if event.key == pygame.K_c:
                game.swap()
            if event.key == pygame.K_LEFT:
                interval_init = 170
                game.left()
                lasttime = pygame.time.get_ticks()
            if event.key == pygame.K_RIGHT:
                interval_init = 170
                game.right()
                lasttime = pygame.time.get_ticks()
            if event.key == pygame.K_DOWN:
                interval_init = 170
                game.soft_drop()
                lasttime = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()  #checking pressed keys
    if pygame.time.get_ticks() > lasttime + interval_init:
        interval_init = 0
        if pygame.time.get_ticks() > lasttime + interval:
            if keys[pygame.K_LEFT]:
                game.left()
            if keys[pygame.K_RIGHT]:
                game.right()
            if keys[pygame.K_DOWN]:
                game.soft_drop(1)
            lasttime = pygame.time.get_ticks()
    # Fill the background with white
    screen.fill((255, 255, 255))
    draw_piece(screen, pieceToNum(game.hold), 100, 250, 100, 100)
    text_surface = my_font.render("Hold", False, (0, 0, 0))
    screen.blit(text_surface, (125, 200))
    text_surface2 = my_font.render("Next Queue", False, (0, 0, 0))
    screen.blit(text_surface2, (580, 100))
    
    # Next Queue
    next_yposes = [150, 250, 350, 450, 550]
    pygame.draw.rect(screen, (0, 0, 0), (600, next_yposes[0], 75, 75), 5)
    pygame.draw.rect(screen, (0, 0, 0), (600, next_yposes[1], 75, 75), 5)
    pygame.draw.rect(screen, (0, 0, 0), (600, next_yposes[2], 75, 75), 5)
    pygame.draw.rect(screen, (0, 0, 0), (600, next_yposes[3], 75, 75), 5)
    pygame.draw.rect(screen, (0, 0, 0), (600, next_yposes[4], 75, 75), 5)
    for i in range(5):
        draw_piece(screen, pieceToNum(game.queue[i]), 600, next_yposes[i], 75, 75)
    # Hold
    pygame.draw.rect(screen, (0, 0, 0), (100, 250, 100, 100), 5)

    game.tick()
    board = game.get_playfield().tolist()
    grid = [[colorDict[board[j][i]] for i in range(10)] for j in range(20)]
    draw_grid(screen, 20, 10)
    pygame.draw.rect(screen, (150, 150, 150), (top_left_x, top_left_y, play_width, play_height), 5)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()