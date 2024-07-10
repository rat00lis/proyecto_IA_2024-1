from visual import Game2048
from agent import agent
import pygame

agent = agent(0, 0, 0, 0)
agent.load_agent()
GAME = Game2048()
while True:
    move = agent.get_move(GAME.game.get_score(), GAME.game.get_matrix())
    if move == 0:
        movement = 'down'
    elif move == 1:
        movement = 'up'
    elif move == 2:
        movement = 'left'
    elif move == 3:
        movement = 'right'
    GAME.run_step(movement)
    #delay
    pygame.time.delay(100)
    while GAME.game.game_over() is not None:
        #wait for enter to restart
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    GAME.restart_game()
                    break
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()