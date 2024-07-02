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
pygame.display.set_caption('2048 Game')
font = pygame.font.Font('fonts/ClearSans-Bold.ttf', 30)
primary_font_color = '#776e65'

def get_font_settings(cell):
    settings = {
        'background_color': (0, 0, 0),
        'font_color': (255, 255, 255),
        'font_size': 30,
    }
    if cell == 0:
        settings['background_color'] = '#cdc1b4'
        settings['font_color'] = '#776e65'
        settings['font_size'] = 30
    if cell == 2:
        settings['background_color'] = '#eee4da'
        settings['font_color'] = '#776e65'
        settings['font_size'] = 60
    elif cell == 4:
        settings['background_color'] = '#ede0c8'
        settings['font_color'] = '#776e65'
        settings['font_size'] = 60
    elif cell == 8:
        settings['background_color'] = '#f2b179'
        settings['font_color'] = '#f9f6f2'
        settings['font_size'] = 60
    elif cell == 16:
        settings['background_color'] = '#f59563'
        settings['font_color'] = '#f9f6f2'
        settings['font_size'] = 60
    elif cell == 32:
        settings['background_color'] = '#f67c5f'
        settings['font_color'] = '#f9f6f2'
        settings['font_size'] = 60
    elif cell == 64:
        settings['background_color'] = '#f65e3b'
        settings['font_color'] = '#f9f6f2'
        settings['font_size'] = 60
    elif cell == 128:
        settings['background_color'] = '#edcf72'
        settings['font_color'] = '#f9f6f2'
        settings['font_size'] = 50
    elif cell == 256:
        settings['background_color'] = '#edcc61'
        settings['font_color'] = '#f9f6f2'
        settings['font_size'] = 50
    elif cell == 512:
        settings['background_color'] = '#edc850'
        settings['font_color'] = '#f9f6f2'
        settings['font_size'] = 50
    elif cell == 1024:
        settings['background_color'] = '#edc53f'
        settings['font_color'] = '#f9f6f2'
        settings['font_size'] = 40
    elif cell == 2048:
        settings['background_color'] = '#edc22e'
        settings['font_color'] = '#f9f6f2'
        settings['font_size'] = 40
    
    return settings

running = True
while running:
    background_color = '#faf8ef'

    # Verificar si el juego ha terminado
    if game.game_over() != None:
        screen.fill(background_color)
        # Si el juego ha terminado, mostrar el mensaje correspondiente
        font = pygame.font.Font('fonts/ClearSans-Bold.ttf', 30)
        finish_text = 'Game over' if not game.game_over() else 'You win'
        text = font.render(finish_text, True, primary_font_color)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
        screen.blit(text, text_rect)

        text = font.render('Score: ' + str(game.get_score()), True,primary_font_color)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2-20))
        screen.blit(text, text_rect)

        text = font.render('Press space to restart', True, primary_font_color)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
        screen.blit(text, text_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.restart()
        continue

    flag = False
    screen.fill(background_color)
    windowWidth = WIDTH
    windowHeight = HEIGHT
    num_rows = len(game.matrix)
    num_cols = len(game.matrix[0])
    margin = 10
    cell_margin = 10  # Espacio entre las celdas
    total_margin = (num_cols + 1) * cell_margin
    score_height = 50  # Espacio para el puntaje
    cellSize = (min((windowWidth - margin * 2 - total_margin) // num_cols, (windowHeight - margin * 2 - total_margin - score_height) // num_rows))
    horizontal = cellSize * num_cols + (num_cols + 1) * cell_margin
    vertical = cellSize * num_rows + (num_rows + 1) * cell_margin
    matrixStartX = windowWidth // 2 - horizontal // 2
    matrixStartY = windowHeight // 2 - vertical // 2 + score_height // 2  # Ajustar para dejar espacio para el puntaje

    # agregar texto "2048" en la parte superior izquierda
    font2048 = pygame.font.Font('fonts/ClearSans-Bold.ttf', 50)
    text2048 = font2048.render('2048', True, '#776e65')
    text2048_rect = text2048.get_rect(topleft=(matrixStartX, matrixStartY - score_height // 2 - margin*4))
    screen.blit(text2048, text2048_rect)


    # Pintar el puntaje en la parte superior derecha
    fontScore = pygame.font.Font('fonts/ClearSans-Bold.ttf', 25)
    textScore = fontScore.render('Score: ' + str(game.get_score()), True, (255, 255, 255))
    textScore_rect = textScore.get_rect(topleft=(matrixStartX + horizontal - textScore.get_width(), matrixStartY - score_height // 2 - margin))
    # Dibujar rectángulo según el tamaño del texto
    score_position_x = matrixStartX + horizontal - textScore.get_width() - margin  # Añade 'margin' para asegurar un espacio entre el puntaje y la matriz
    # Calcula la posición Y del puntaje para que esté arriba de la matriz con un margen adecuado
    score_position_y = matrixStartY - score_height // 2 - margin * 2  # Añade un margen adicional si es necesario
    textScore_rect.topleft = (score_position_x, score_position_y)
    pygame.draw.rect(screen, '#bbada0', (textScore_rect.x - 10, textScore_rect.y - 5, textScore_rect.width + 20, textScore_rect.height + 10), border_radius=5)
    screen.blit(textScore, textScore_rect)


    # Pintar un cuadro debajo de la grilla
    pygame.draw.rect(screen, '#bbada0', (matrixStartX, matrixStartY, horizontal, vertical), border_radius=5)

    for i in range(num_rows):
        for j in range(num_cols):
            cell = game.matrix[i][j]
            cell_settings = get_font_settings(cell)
            fontNumbers = pygame.font.Font('fonts/ClearSans-Bold.ttf', cell_settings['font_size'])
            cell_x = matrixStartX + (j + 1) * cell_margin + j * cellSize
            cell_y = matrixStartY + (i + 1) * cell_margin + i * cellSize
            pygame.draw.rect(screen, cell_settings['background_color'], (cell_x, cell_y, cellSize, cellSize), border_radius=5)
            text = fontNumbers.render(str(cell) if cell != 0 else "", True, cell_settings['font_color'])
            text_rect = text.get_rect(center=(cell_x + cellSize // 2, cell_y + cellSize // 2))
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
