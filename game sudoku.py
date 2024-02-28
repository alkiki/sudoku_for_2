from copy import deepcopy
import pygame
from funcs import draw_9x9_board, drawing_game_status, drawing_timer, \
    drawing_result, get_initial_finish_grid, draw_numbers, get_square_selected, \
    evidence_value_selected, drawing_winner


width = 600  # width of the window
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)

how_big_square = 50  # the size of the square
position_board_on_window = (75, 75)
font_name = "Consolas"
big_size_font = 35
medium_size_font = 20
small_size_font = 15
level_of_difficulty = 0
seconds_per_round = 60

color_menu_bottom = '#383ea9'
color_evidence = (0, 255, 0, 50)

color_surface_board = 'white'
players = [
    {
        'name': 'player1',
        'selected': [[0 for el in range(1, 10)] for row in range(1, 10)],  # grid with 0s to store the correct values from the player1
        'color': '#E24F4F',
        'score': 0,
    },
    {
        'name': 'player2',
        'selected': [[0 for el in range(1, 10)] for row in range(1, 10)],  # grid with 0s to store the correct values from the player2
        'color': '#E2A74F',
        'score': 0,
    },
]


def main():
    main_window = pygame.display.set_mode((width, width))  # displaying the window
    pygame.display.set_caption('Sudoku')
    main_window.fill(background_color)
    myfont_big = pygame.font.SysFont(font_name, big_size_font)
    myfont_medium = pygame.font.SysFont(font_name, medium_size_font)
    myfont_small = pygame.font.SysFont(font_name, small_size_font)
    # the result of the function that will give us the initial grid
    intro = True
    while intro:  # the loop that will display the instructions and button to start playing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        main_window.fill((251, 247, 245))  # filling the background

        #  tlines 58 -111 were written based on a yuotube tutorial on how to create a menu with buttons and add interaction to them. URL: https://youtu.be/P-UuVITG7Vg
        def instruction(text, x, y):
            instructions = myfont_small.render(text, True, 'black')
            main_window.blit(instructions, instructions.get_rect(
                                     center=(x, y)))

        instruction('Sudoku for 2 players! Each player has a 1 minute limit', 285, 160)
        instruction('to fill in as many cells of the', 285, 180)
        instruction('sudoku grid with correct values as possible.', 285, 200)
        instruction('After 1 minute, the turn goes to another player.', 285, 220)
        instruction('For each correct input, player get +1 to their', 285, 240)
        instruction('score and for each incorrect value, player gets -1', 285, 260)
        instruction('to their score. Game finishes, when the grid is', 285, 280)
        instruction('completed. The player that gets higher score wins.', 285, 300)
        mouse = pygame.mouse.get_pos()  # getting the position of the mouse
        click = pygame.mouse.get_pressed()  # the data collected if the mouse is clicked
        instructions4 = myfont_small.render(
                    'Choose level of difficulty:', True, 'black')
        main_window.blit(instructions4, instructions4.get_rect(center=(300, 330)))
        # creating three buttons for choosing the difficulty level of initial sudoku grid
        if 220+100 > mouse[0] > 220 and 350 + 50 > mouse[1] > 350:  # if the mouse is within the rectangle
            pygame.draw.rect(main_window, (0, 200, 0), (220, 350, 150, 50))  # change the color of the rectangle to light green for interactivity
            if click[0] == 1:  # if the mouse is clicked within the rectangle, then we quit the menu and start the game
                level_of_difficulty = 2
                intro = False
        else:
            pygame.draw.rect(main_window, (0, 102, 0), (220, 350, 150, 50))  # the color is green
        text_on_the_button = myfont_medium.render(
                    'Medium', True, 'black')
        main_window.blit(text_on_the_button,
                         text_on_the_button.get_rect(center=(295, 375)))
        if 50+100 > mouse[0] > 50 and 350 + 50 > mouse[1] > 350:
            pygame.draw.rect(main_window, (255, 229, 204), (50, 350, 150, 50))
            if click[0] == 1:  # if the mouse is clicked within the rectangle, then we quit the menu and start the game
                level_of_difficulty = 1
                intro = False
        else:
            pygame.draw.rect(main_window, (255, 204, 153), (50, 350, 150, 50))
        text_on_the_button = myfont_medium.render(
                    'Easy', True, 'black')
        main_window.blit(text_on_the_button,
                         text_on_the_button.get_rect(center=(128, 375)))
        if 390+100 > mouse[0] > 390 and 350 + 50 > mouse[1] > 350:
            pygame.draw.rect(main_window, (255, 102, 102), (390, 350, 150, 50))
            if click[0] == 1:  # if the mouse is clicked within the rectangle, then we quit the menu and start the game
                level_of_difficulty = 3
                intro = False
        else:
            pygame.draw.rect(main_window, (204, 0, 0), (390, 350, 150, 50))
        text_on_the_button = myfont_medium.render(
                    'Hard', True, 'black')
        main_window.blit(text_on_the_button,
                         text_on_the_button.get_rect(center=(465, 375)))

        pygame.display.update()
        pygame.time.Clock().tick(15)
    initial_grid, solution_grid = get_initial_finish_grid(level_of_difficulty)
    working_grid = deepcopy(initial_grid)  # making the copy of the initial grid so we can update it while the game is on

    clock = pygame.time.Clock()  # clock

    selected = None

    while working_grid != solution_grid:  # until the grid is completed
        for player in players:
            if working_grid == solution_grid:  # if the grid is completed then the game ends
                break
            # the counter of the time
            remain_time = seconds_per_round
            pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1 second
            while remain_time and working_grid != solution_grid:  # until the timer has not run out and the grid is not completed

                squares_9x9 = draw_9x9_board(pygame, how_big_square, color_surface_board)  # drawing the lines in the window

                main_window.fill(background_color)  # filling the background
                render_text_start1 = myfont_big.render(
                    'Sudoku for 2 players!', True, 'black')
                main_window.blit(render_text_start1,
                                 render_text_start1.get_rect(
                                     center=(300, 30)))  # displaying the text in a designated position

                if selected:
                    evidence_value_selected(pygame,
                                            selected,
                                            squares_9x9,
                                            how_big_square,
                                            color_evidence)  # highlighting the square
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.USEREVENT:
                        remain_time -= 1  # if the event happened, the timer goes down 1 second

                    if event.type == pygame.MOUSEBUTTONUP:
                        value, row, el = get_square_selected(  # value, row and element
                            pygame,
                            working_grid,
                            position_board_on_window,
                            how_big_square)
                        if not value:  # if 0 that we can input, otherwise no
                            selected = (value, row, el)
                        else:
                            selected = None  # otherwise nothing happens
                    if selected:
                        if event.type == pygame.KEYDOWN:
                            if pygame.key.name(event.key) in '123456789':
                                key_to_input = pygame.key.name(event.key)
                                if solution_grid[selected[1]][selected[2]] == int(key_to_input):  # if the value from  the player is correct
                                    working_grid[selected[1]][selected[2]] = int(key_to_input)  # save that info to the working grid
                                    player['score'] += 1  # score goes up
                                    player['selected'][selected[1]][selected[2]] = int(key_to_input)  # updating the grid for player1 to keep track which vvalues he inputted correctly
                                else:
                                    player['score'] -= 1  # score goes down
                                selected = None
                # at the end of each while loop, we are drawing the table again
                drawing_game_status(pygame, main_window, player, myfont_medium)

                drawing_result(pygame, main_window, player, myfont_medium, color_menu_bottom)
                drawing_timer(pygame, remain_time, main_window, myfont_medium, color_menu_bottom)
                draw_numbers(pygame,
                             squares_9x9,
                             player,
                             initial_grid,
                             original_grid_element_color,
                             working_grid,
                             myfont_big,
                             how_big_square)

                main_window.blit(squares_9x9, position_board_on_window)
                pygame.display.flip()  # Updating the full display Surface to the screen
                clock.tick(60)  # updating the timer

    while True:
        winner = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if players[0]['score'] > players[1]['score']:  # if the score of player1 by the end of the game is higher than the score of player 2 then player 1 wins
            winner = players[0]
        elif players[0]['score'] < players[1]['score']:  # if the score of player2 by the end of the game is higher than the score of player1 then player 2 wins
            winner = players[1]
        elif players[0]['score'] == players[1]['score']:  # if the scores are even, that means that friendship won
            winner = 'friendship'
        main_window.fill(background_color)  # filling the window
        render_text_start1 = myfont_big.render(
            'Sudoku for 2 players!', True, 'black')
        main_window.blit(render_text_start1,
                         render_text_start1.get_rect(
                             center=(300, 30)))
        drawing_winner(pygame, main_window, winner, myfont_big)
        pygame.display.flip()  # updating the content of the display


if __name__ == '__main__':
    # implementing the code
    pygame.init()
    main()
    pygame.quit()
