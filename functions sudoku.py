from dokusan import generators, solvers
from dokusan.boards import BoxSize, Sudoku


level_of_difficulty = 0

def draw_9x9_board(pygame, how_big_square, color_surface_board):
    #   drawing the 9x9 board
    #   new surface
    surface = pygame.Surface(
        (how_big_square * 9 + 2, how_big_square * 9 + 2))
    # the color of the surface
    surface.fill(pygame.Color(color_surface_board))

    for i in range(10):
        # drawing lines of the grid
        # the code for sudoku gridline (lines 15-28) wass written based on the youtube tutorial URL: https://youtu.be/I2lOwRiGNy4, (2:02 - 7:20)
        if i % 3 == 0:  # each third line is heavy line to indicate 3x3 boxes
            pygame.draw.line(surface, (0, 0, 0), (how_big_square * i, 0),
                             (how_big_square * i, 500), 4)
            pygame.draw.line(surface, (0, 0, 0), (0, how_big_square * i),
                             (500, how_big_square * i), 4)
        else:
            pygame.draw.line(surface, (0, 0, 0), (how_big_square * i, 0),
                             (how_big_square * i, 500), 1)
            pygame.draw.line(surface, (0, 0, 0), (0, how_big_square * i),
                             (500, how_big_square * i), 1)
    return surface


def get_square_selected(pygame, working_grid, position_board_on_window, how_big_square):
    # getting the value, position of the selected cell by using 2-dimensional vector function
    mouse_positions = pygame.Vector2(
        pygame.mouse.get_pos()) - position_board_on_window  # position of the coursor
    list_positions = []
    for position in mouse_positions:
        list_positions.append(int(position // how_big_square))  # position of element and value so we can acess the solver grid and compare
    el, row = list_positions
    try:  # trying if the el and row are > 0
        if el >= 0 and row >= 0:
            return working_grid[row][el], row, el
    except Exception as e:  # exception in case they are < 0, then we just pass
        pass
    return None, None, None


def get_initial_finish_grid(level_of_difficulty):
    # generating initial grid and solves one
    element_per_row = 9
    if level_of_difficulty == 1:
        initial_str = str(generators.random_sudoku(avg_rank=30))  # generating initial grid, 30 is the level of difficulty
    if level_of_difficulty == 2:
        initial_str = str(generators.random_sudoku(avg_rank=80))
    if level_of_difficulty == 3:
        initial_str = str(generators.random_sudoku(avg_rank=150))
    sudoku_to_solv = Sudoku.from_string(initial_str, box_size=BoxSize(3, 3))  # we get a string of all the numbers for initial sudoku
    solution_str = str((solvers.backtrack(sudoku_to_solv)))  # the solution for the current sudoku

    list_initial = list(map(int, initial_str))  # transferring each value to int type and creating a list
    list_solution = list(map(int, solution_str))  # transferring each value of the solved grid to integers
    initial_list = [list_initial[i:i + element_per_row] for i in range(0, len(list_initial), element_per_row)]  # range(start, stop, step)
    solution_list = [list_solution[i:i + element_per_row] for i in range(0, len(list_solution), element_per_row)]  # rendering and creating 9 lists within 1 list so we can access each value by row and position within the row
    return initial_list, solution_list


def draw_numbers(
        pygame,
        squares_9x9,
        player_obj,
        initial_grid,
        original_grid_element_color,
        working_grid,
        myfont,
        how_big_square):
    # putting numbers on the board with different colors
    for row in range(0, len(working_grid)):
        for el in range(0, len(working_grid[row])):
            pos = pygame.Rect(
                el * how_big_square,
                row * how_big_square,
                how_big_square,
                how_big_square)
            color = 'black'
            if initial_grid[row][el]:
                color = original_grid_element_color  # if the value was in the grid initially, the color is blue
            if player_obj['selected'][row][el]:  # if the value has been input by the player, based on the player, we choose the color
                color = player_obj['color']
            if working_grid[row][el]:
                numb_to_draw = myfont.render(
                    str(working_grid[row][el]),
                    True,
                    pygame.Color(color))
                squares_9x9.blit(numb_to_draw, numb_to_draw.get_rect(
                    center=pos.center))


def drawing_game_status(pygame, screen, player_obj, my_font):
    # drawing whose turn it is
    to_render = my_font.render(
        f'Turn: {player_obj["name"]}', True,
        pygame.Color(player_obj['color']))
    screen.blit(to_render, to_render.get_rect(center=(150, 560)))


def drawing_winner(pygame, screen, player_obj, my_font):
    # drawing the winner
    to_render = my_font.render(
        f'Winner: {player_obj["name"]}', True,
        pygame.Color(player_obj['color']))
    screen.blit(to_render, to_render.get_rect(center=(300, 300)))  # displaying the winner

    to_render = my_font.render(
        f'Score: {player_obj["score"]}', True,
        pygame.Color(player_obj['color']))  # defining the score
    screen.blit(to_render, to_render.get_rect(center=(300, 400)))  # displaying the score


def drawing_timer(pygame, remain_time, screen, my_font, color_menu_bottom):
    # creating the timer
    to_render = my_font.render(
        f"""Seconds: {remain_time}""", True,
        pygame.Color(color_menu_bottom))
    screen.blit(to_render, to_render.get_rect(center=(300 + 1, 560)))  # displaying the timer


def drawing_result(pygame, screen, player_obj, my_font, color_menu_bottom):
    # output of the score
    to_render = my_font.render(
        f'Socre: {player_obj["score"]}', True,
        pygame.Color(color_menu_bottom))
    screen.blit(to_render, to_render.get_rect(center=(450 + 2, 560)))


def evidence_value_selected(pygame, selected, squares_9x9, how_big_square, color_evidence):
    # function that highlights the selected cell
    value, row, el = selected
    if row is not None:
        rect = (
            el * how_big_square,
            row * how_big_square,
            how_big_square,
            how_big_square)
        pygame.draw.rect(squares_9x9, color_evidence, rect, 2)
