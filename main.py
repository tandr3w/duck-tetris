from random import randint
import tetris
import time
import pygame
import random
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
 
colorDict = {0: (8, 8, 10), 1: (19, 249, 211), 2: (19, 57, 249), 3: (249, 134, 19), 4: (249, 211, 19), 5: (57, 249, 19),
             6: (119, 19, 249), 7: (249, 19, 57), 8: (28, 31, 33), 9: (128, 128, 128)}
 
colorDictP = {0: (8, 8, 10), 1: (100, 100, 100), 2: (100, 100, 100), 3: (100, 100, 100), 4: (100, 100, 100),
              5: (100, 100, 100), 6: (100, 100, 100), 7: (100, 100, 100), 8: (8, 8, 10), 9: (100, 100, 100)}
 
pieceGrid = {
    None: [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]],
    1: [[0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]],
    2: [[2, 0, 0, 0],
        [2, 2, 2, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]],
    3: [[0, 0, 3, 0],
        [3, 3, 3, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]],
    4: [[0, 4, 4, 0],
        [0, 4, 4, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]],
    5: [[0, 0, 5, 5],
        [0, 5, 5, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]],
    6: [[0, 6, 0, 0],
        [6, 6, 6, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]],
    7: [[7, 7, 0, 0],
        [0, 7, 7, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]],
}
 
 
def tetriminoNum(piece):
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
    if piece is None:
        return None
 
 
s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
pygame.init()
screen = pygame.display.set_mode([s_width, s_height])
running = True
 
def draw_piece(surface, piece, topLeftX, topLeftY, width, length):
    topLeftX += 5
    topLeftY += 5
    width -= 5
    length -= 5
    piece_width = width // 4
    piece_height = length // 4
    pGrid = pieceGrid[piece]
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(surface, colorDict[pGrid[i][j]], (topLeftX + j * piece_width, topLeftY + i * piece_height, piece_width, piece_height), 0)
 
 
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (18, 20, 22), (sx, sy + i * 30 - 50), (sx + play_width - 1, sy + i * 30 - 50)) 
        for j in range(col):
            pygame.draw.line(surface, (18, 20, 22), (sx + j * 30, sy - 50), (sx + j * 30, sy + play_height - 1 - 50)) 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == (8, 8, 10):
                continue
            pygame.draw.rect(surface, grid[i][j], (sx + j * 30, sy + i * 30 - 50, 30, 30), 0)
 
 
lasttime = 0
interval = 50
interval_init = 170
pygame.font.init()
my_font = pygame.font.SysFont(None, 42)
 
duck_show_time = 500
duck_showing = False
manyDucks = False
last_duck_show = pygame.time.get_ticks()
last_manyducks_show = pygame.time.get_ticks()
duckLoc = 0
while running:
    screen.fill((20, 10, 12))
    action = randint(1, 5000)
    duck = pygame.transform.scale(pygame.image.load("duck" + str(randint(0, 1)) + ".png"), (300, 300))
    if last_manyducks_show + duck_show_time < pygame.time.get_ticks():
        manyDucks = False
    if last_duck_show + duck_show_time < pygame.time.get_ticks():
        duck_showing = False
    if action < 10:
        last_duck_show = pygame.time.get_ticks()
        duck_showing = True
        duckLoc = (randint(0, 700), randint(0, 700))
    if action == 1:
        # make duck way bigger
        last_manyducks_show = pygame.time.get_ticks()
        manyDucks = True
    elif action == 2:
        game.soft_drop(3)
    elif action == 3:
        if game.hold == None:
            action = randint(4, 9)
        game.hold = None
    elif action == 4:
        game.level += 3
    elif action == 5:
        game.queue.fill()
    elif action == 6:
        game.left(randint(1, 10))
        game.right(randint(1, 10))
        game.rotate(randint(1, 10))
        game.hard_drop()
    elif action == 7:
        for i in range(18, len(game.board)):
            if i == 39:
                game.board[39] = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
                game.board[39][randint(0, 9)] = 0
            else:
                game.board[i] = game.board[i+1]

    elif action == 8:
        game.swap()
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.reset()
                game = tetris.BaseGame()
            if event.key == pygame.K_ESCAPE:
                game.pause()
            if event.key == pygame.K_SPACE:
                game.hard_drop()
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_x:
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
 
    keys = pygame.key.get_pressed()  # checking pressed keys
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
 
    draw_piece(screen, tetriminoNum(game.hold), 100, 55, 100, 100)
 
    text_surface = my_font.render(str(game.score), True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(s_width // 2 - 100, s_height - 25))
    screen.blit(text_surface, text_rect)
 
    text_surface2 = my_font.render(str(game.level), True, (255, 255, 255))
    text_rect2 = text_surface2.get_rect(center=(s_width // 2 + 100, s_height - 25))
    screen.blit(text_surface2, text_rect2)
 
    next_yposes = [55, 140, 225, 310, 395]
    pygame.draw.rect(screen, (50, 55, 59), (600, next_yposes[0], 80, 80), 5, 5)
    pygame.draw.rect(screen, (50, 55, 59), (600, next_yposes[1], 80, 80), 5, 5)
    pygame.draw.rect(screen, (50, 55, 59), (600, next_yposes[2], 80, 80), 5, 5)
    pygame.draw.rect(screen, (50, 55, 59), (600, next_yposes[3], 80, 80), 5, 5)
    pygame.draw.rect(screen, (50, 55, 59), (600, next_yposes[4], 80, 80), 5, 5)
 
    for i in range(5):
        draw_piece(screen, tetriminoNum(game.queue[i]), 600, next_yposes[i], 80, 80)
 
    pygame.draw.rect(screen, (50, 55, 59), (100, 55, 100, 100), 5, 5)
 
    game.tick()
    board = game.get_playfield().tolist()
    if game.paused or game.lost:
        grid = [[colorDictP[board[j][i]] for i in range(10)] for j in range(20)]
    else:
        grid = [[colorDict[board[j][i]] for i in range(10)] for j in range(20)]
    draw_grid(screen, 20, 10)
    pygame.draw.rect(screen, (50, 55, 59), (top_left_x-5, top_left_y-55, play_width+10, play_height+10), 5, 5)
    if duck_showing:
        screen.blit(duck, duckLoc)
    if manyDucks:
        screen.blit(duck, (randint(-700, 700), randint(-700, 700)))
        screen.blit(duck, (randint(-700, 700), randint(-700, 700)))
        screen.blit(duck, (randint(-700, 700), randint(-700, 700)))
        screen.blit(duck, (randint(-700, 700), randint(-700, 700)))
        screen.blit(duck, (randint(-700, 700), randint(-700, 700)))
        screen.blit(duck, (randint(-700, 700), randint(-700, 700)))
    pygame.display.flip()
 
 
pygame.quit()