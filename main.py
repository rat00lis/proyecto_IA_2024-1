import pygame
import copy
import argparse
from matrix import matrix_2048

parser = argparse.ArgumentParser(description='Run 2048 game with specified algorithm.')
parser.add_argument('--algorithm', type=str, help='Algorithm to use: mcts, genetic or dqn', default='none')
args = parser.parse_args()

if args.algorithm == 'mcts':
    from MCTS.randomRollouts import MCTS2048
    MCTS_agent = MCTS2048(rollouts_number=100, avg_evaluations=0, eval_function=0)
if args.algorithm == 'genetic':
    from genetico.agent import agent as Genetic_agent
    genetic_agent = Genetic_agent(population_size=0, genome_size=0, mutation_rate=0, tree_height=0)
    genetic_agent.load_agent()
elif args.algorithm == 'dqn':
    from DQN.DQN_agent import DQN_Agent
    DQN_agent = DQN_Agent()

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

def draw_game_board(screen, matrix, num_rows, num_cols, matrixStartX, matrixStartY, horizontal, vertical, margin, cellSize):
    # Fondo de matriz
    pygame.draw.rect(screen, '#bbada0', (matrixStartX, matrixStartY, horizontal, vertical), border_radius=5)

    # Celdas matriz
    for i in range(num_rows):
        for j in range(num_cols):
            cell = matrix[i][j]
            cell_settings = get_font_settings(cell)
            fontNumbers = pygame.font.Font('fonts/ClearSans-Bold.ttf', cell_settings['font_size'])
            cell_x = matrixStartX + (j + 1) * margin + j * cellSize
            cell_y = matrixStartY + (i + 1) * margin + i * cellSize
            pygame.draw.rect(screen, cell_settings['background_color'], (cell_x, cell_y, cellSize, cellSize), border_radius=5)
            text = fontNumbers.render(str(cell) if cell != 0 else "", True, cell_settings['font_color'])
            text_rect = text.get_rect(center=(cell_x + cellSize // 2, cell_y + cellSize // 2))
            screen.blit(text, text_rect)

def draw_game_over(screen, game, WIDTH, HEIGHT):
    font = pygame.font.Font('fonts/ClearSans-Bold.ttf', 30)
    finish_text = 'Game over' if not game.game_over() else 'You win'
    text = font.render(finish_text, True, primary_font_color)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
    screen.blit(text, text_rect)

    text = font.render('Score: ' + str(game.get_score()), True,(primary_font_color))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2-20))
    screen.blit(text, text_rect)

    text = font.render('Press space to restart', True, primary_font_color)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    screen.blit(text, text_rect)

    pygame.display.flip() 

def draw_game_layout(screen, game):
    # Texto 2048
    font2048 = pygame.font.Font('fonts/ClearSans-Bold.ttf', 50)
    text2048 = font2048.render('2048', True, primary_font_color)
    text2048_rect = text2048.get_rect(topleft=(matrixStartX, matrixStartY - score_height // 2 - margin*4))
    screen.blit(text2048, text2048_rect)

    # Score
    fontScore = pygame.font.Font('fonts/ClearSans-Bold.ttf', 25)
    textScore = fontScore.render('Score: ' + str(game.get_score()), True, (255,255,255))
    textScore_rect = textScore.get_rect(topleft=(matrixStartX + horizontal - textScore.get_width(), matrixStartY - score_height // 2 - margin))
    score_position_x = matrixStartX + horizontal - textScore.get_width() - margin
    score_position_y = matrixStartY - score_height // 2 - margin * 2  
    textScore_rect.topleft = (score_position_x, score_position_y)
    pygame.draw.rect(screen, '#bbada0', (textScore_rect.x - 10, textScore_rect.y - 5, textScore_rect.width + 20, textScore_rect.height + 10), border_radius=5)
    screen.blit(textScore, textScore_rect)

game = matrix_2048()

# Window setting
WIDTH = 700
HEIGHT = 600

# Matrix setting
num_rows = len(game.matrix)
num_cols = len(game.matrix[0])
margin = 10
total_margin = (num_cols + 1) * margin
score_height = 50  # Espacio para el puntaje
cellSize = (min((WIDTH - margin * 2 - total_margin) // num_cols, (HEIGHT - margin * 2 - total_margin - score_height) // num_rows))
horizontal = cellSize * num_cols + (num_cols + 1) * margin
vertical = cellSize * num_rows + (num_rows + 1) * margin
matrixStartX = WIDTH // 2 - horizontal // 2
matrixStartY = HEIGHT // 2 - vertical // 2 + score_height // 2  # Ajustar para dejar espacio para el puntaje

# Initialize font
pygame.font.init()
font = pygame.font.Font('fonts/ClearSans-Bold.ttf', 30)
primary_font_color = '#776e65'

# Initialize game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 Game')

running = True
while running:
    background_color = '#faf8ef'
    screen.fill(background_color)

    # Verificar si el juego ha terminado
    if game.game_over() != None:
        #draw_game_over(screen, game, WIDTH, HEIGHT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.restart()
        draw_game_layout(screen, game)
        draw_game_board(screen, game.matrix, num_rows, num_cols, matrixStartX, matrixStartY, horizontal, vertical, margin, cellSize)
        pygame.display.flip()
        continue
    
    draw_game_layout(screen, game)
    draw_game_board(screen, game.matrix, num_rows, num_cols, matrixStartX, matrixStartY, horizontal, vertical, margin, cellSize)

    valid_movement = False
    if args.algorithm == 'none':
        # Eventos
        previous_matrix = copy.deepcopy(game.matrix)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'w' or key == 'up': valid_movement = game.up()
                elif key == 's' or key == 'down': valid_movement = game.down()
                elif key == 'a' or key == 'left': valid_movement = game.left()
                elif key == 'd' or key == 'right': valid_movement = game.right()
    
    elif args.algorithm == 'mcts':
        best_move = MCTS_agent.select_best_move(game)
        if best_move == 'up': valid_movement = game.up()
        elif best_move == 'down': valid_movement = game.down()
        elif best_move == 'left': valid_movement = game.left()
        elif best_move == 'right': valid_movement = game.right()

    elif args.algorithm == 'genetic':
        best_move = genetic_agent.get_move(game.get_score(), game.matrix)
        if best_move == 0: valid_movement = game.up()
        elif best_move == 1: valid_movement = game.down()
        elif best_move == 2: valid_movement = game.left()
        elif best_move == 3: valid_movement = game.right()
        #pygame.time.delay(100)
    elif args.algorithm == 'dqn':
        action = DQN_agent.select_action(game)
        if action.item() == 0:  valid_movement = game.up()
        elif action.item() == 1: valid_movement =  game.down()
        elif action.item() == 2: valid_movement = game.left()
        elif action.item() == 3: valid_movement = game.right()
        pygame.time.delay(100)
    
    if valid_movement:
        game.add_number()
    
    pygame.display.flip()
pygame.quit()