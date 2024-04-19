import random
import pygame
import copy
import math
from matrix import matrix_2048

game = matrix_2048()

WIDTH = 700
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 30)

running = True
while running:
    flag = False
    screen.fill((255, 255, 255))
    windowWidth = WIDTH
    windowHeight = HEIGHT
    num_rows = len(game.matrix)
    num_cols = len(game.matrix[0])
    margin = 10
    cellSize = min((windowWidth-margin*2) // num_cols,(windowHeight-margin*2)//num_rows)
    horizontal = cellSize*num_cols
    vertical = cellSize*num_rows
    matrixStartX = windowWidth//2 - horizontal//2
    matrixStartY = windowHeight//2 - vertical//2
    for i in range(num_rows):
        for j in range(num_cols):
            cell = game.matrix[i][j]
            if cell != 0:
                fontNumbers = pygame.font.Font(None, (cellSize)//len(str(cell)))
                level = math.log(cell,2)
                color = (255,255,255 - level*23)
                pygame.draw.rect(screen, color, (matrixStartX + j * cellSize, matrixStartY + i * cellSize, cellSize, cellSize))
                text = fontNumbers.render(str(cell), True, (0, 0, 0))
                text_rect = text.get_rect(center=(matrixStartX + j * cellSize + cellSize//2, matrixStartY + i * cellSize + cellSize//2))
                screen.blit(text, text_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key == 'w' or key == 'up': flag = game.up()
            elif key == 's' or key == 'down': flag = game.down()
            elif key == 'a' or key == 'left': flag = game.left()
            elif key == 'd' or key == 'right': flag = game.right()
    if flag:
        game.add_number()
    pygame.display.flip()
pygame.quit()
