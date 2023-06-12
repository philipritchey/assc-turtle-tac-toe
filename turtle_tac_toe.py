'''
play tic-tac-tow with a turtle
'''

########################################
#
# DO NOT CHANGE THIS CODE
#
########################################

from turtle import Turtle, Screen, done
from typing import Tuple
from my_functions import announce_winner_is_o, announce_winner_is_x, make_an_o, make_an_x,\
    make_a_cat, prompt_for_new_game

def draw_line(x_1: float, y_1: float, x_2: float, y_2: float) -> None:
    '''
    draw a line from (x_1, y_1) to (x_2, y_2)
    '''
    TURTLE.penup()
    TURTLE.goto(x_1, y_1)
    TURTLE.setheading(TURTLE.towards(x_2, y_2))
    TURTLE.pendown()
    TURTLE.forward(TURTLE.distance(x_2, y_2))

def draw_board() -> None:
    '''
    3 x 3 grid, middle borders only
    '''

    # center . at (0,0)
    #    |   |
    # ---+---+---
    #    | . |
    # ---+---+---
    #    |   |

    # horizontal
    draw_line(LEFT, TOP - CELL_WIDTH, RIGHT, TOP - CELL_WIDTH)
    draw_line(LEFT, BOTTOM + CELL_WIDTH, RIGHT, BOTTOM + CELL_WIDTH)

    # vertical
    draw_line(LEFT + CELL_WIDTH, TOP, LEFT + CELL_WIDTH, BOTTOM)
    draw_line(RIGHT - CELL_WIDTH, TOP, RIGHT - CELL_WIDTH, BOTTOM)

def is_out_of_bounds(x_coord: float, y_coord: float) -> bool:
    '''
    is the click within the bounds of the board?
    '''
    # board is box ((LEFT, TOP), (RIGHT, BOTTOM))
    return not (LEFT < x_coord < RIGHT
                and BOTTOM < y_coord < TOP)

def get_row_col(coord: float) -> int:
    '''
    convert coordinate into row/col index
    '''
    return min(2, int((coord - LEFT) / CELL_WIDTH))

def get_row(y_coord: float) -> int:
    '''
    convert y-coordinate into row index
    '''
    return get_row_col(y_coord)

def get_column(x_coord: float) -> int:
    '''
    convert x-coordinate to column index
    '''
    return get_row_col(x_coord)

def cell_is_occupied(x_coord: float, y_coord: float) -> bool:
    '''
    is there already a mark in this cell?
    '''
    if is_out_of_bounds(x_coord, y_coord):
        return False

    # x,y are in bounds
    row = get_row(y_coord)
    column = get_column(x_coord)
    return BOARD_STATE[2-row][column] in (X_SYMBOL, O_SYMBOL)

def move_to_cell_bottom_center(turtle, x_coord: float, y_coord: float) -> None:
    '''
    move the turtle to the center of the cell which contains (x, y)
    '''

    #  1 | 2 | 3
    # ---+---+---
    #  4 | 5 | 6
    # ---+---+---
    #  7 | 8 | 9

    if is_out_of_bounds(x_coord, y_coord):
        # do nothing
        return

    # x,y are in bounds
    row = get_row(y_coord)
    column = get_column(x_coord)
    new_x = CELL_WIDTH * (column - 1)
    new_y = CELL_WIDTH * (row - 1)
    turtle.penup()
    turtle.goto(new_x, new_y - CELL_WIDTH / 2)
    turtle.setheading(90)

def row_start(row: int) -> Tuple[float, float]:
    '''
    return coordinates of row start (left edge, middle of row)
    '''
    return LEFT, CELL_WIDTH * (row - 1)

def column_start(column: int) -> Tuple[float, float]:
    '''
    return coordinates of column start (top edge, middle of column)
    '''
    return CELL_WIDTH * (column - 1), TOP

def do_nothing(_xdummy: float, _ydummy: float) -> None:
    '''
    do nothing.
    '''

def draw_winning_line(which: str) -> None:
    '''
    draw the winning line through the 3-in-a-row
    '''
    TURTLE.pensize(int(CELL_WIDTH / 10))
    if which[0] == ROW:
        x_coord, y_coord = row_start(int(which[1]))
        draw_line(x_coord, y_coord, x_coord + BOARD_WIDTH, y_coord)
    elif which[0] == COLUMN:
        x_coord, y_coord = column_start(int(which[1]))
        draw_line(x_coord, y_coord, x_coord, y_coord - BOARD_WIDTH)
    elif which == FORWARD_DIAGONAL:
        draw_line(LEFT, TOP, RIGHT, BOTTOM)
    elif which == BACKWARD_DIAGONAL:
        draw_line(RIGHT, TOP, LEFT, BOTTOM)
    else:
        raise ValueError(f'no such winning line type: {which}')

def x_wins(which: str) -> None:
    '''
    show that 'X' wins
    '''
    SCREEN.onscreenclick(do_nothing)
    TURTLE.pencolor('red')
    draw_winning_line(which)

    STUDENT_TURTLE.penup()
    STUDENT_TURTLE.goto(0, 0)
    STUDENT_TURTLE.setheading(90)
    announce_winner_is_x(STUDENT_TURTLE, CELL_WIDTH)

def o_wins(which: str) -> None:
    '''
    show that 'O' wins
    '''
    SCREEN.onscreenclick(do_nothing)
    TURTLE.pencolor('green')
    draw_winning_line(which)

    STUDENT_TURTLE.penup()
    STUDENT_TURTLE.goto(0, 0)
    STUDENT_TURTLE.setheading(90)
    announce_winner_is_o(STUDENT_TURTLE, CELL_WIDTH)

def cat_wins() -> None:
    '''
    show that it's a tie game
    '''
    SCREEN.onscreenclick(do_nothing)

    STUDENT_TURTLE.penup()
    STUDENT_TURTLE.goto(0, 0)
    STUDENT_TURTLE.setheading(90)
    make_a_cat(STUDENT_TURTLE, CELL_WIDTH)

def check_for_row_win(row: int) -> bool:
    '''
    check for a win in a row
    '''
    if BOARD_STATE[row][0] == BOARD_STATE[row][1] and BOARD_STATE[row][1] == BOARD_STATE[row][2]:
        if BOARD_STATE[row][0] == X_SYMBOL:
            x_wins(f'r{2-row}')
        elif BOARD_STATE[row][0] == O_SYMBOL:
            o_wins(f'r{2-row}')
        else:
            return False
        return True
    return False

def check_for_column_win(column: int) -> bool:
    '''
    check for a win in a column
    '''
    if (BOARD_STATE[0][column] == BOARD_STATE[1][column]
            and BOARD_STATE[1][column] == BOARD_STATE[2][column]):
        if BOARD_STATE[0][column] == X_SYMBOL:
            x_wins(f'c{column}')
        elif BOARD_STATE[0][column] == O_SYMBOL:
            o_wins(f'c{column}')
        else:
            return False
        return True
    return False

def check_for_win() -> bool:
    '''
    check for a win (3-in-a-row) and end game if found
    '''
    # non-diagonals: rows and columns
    for index in range(3):
        if check_for_row_win(index) or check_for_column_win(index):
            return True

    # diagonals
    if BOARD_STATE[0][0] == BOARD_STATE[1][1] and BOARD_STATE[1][1] == BOARD_STATE[2][2]:
        if BOARD_STATE[0][0] == X_SYMBOL:
            x_wins(f'{FORWARD_DIAGONAL}')
        elif BOARD_STATE[0][0] == O_SYMBOL:
            o_wins(f'{FORWARD_DIAGONAL}')
        else:
            return False
        return True
    if BOARD_STATE[0][2] == BOARD_STATE[1][1] and BOARD_STATE[1][1] == BOARD_STATE[2][0]:
        if BOARD_STATE[0][2] == X_SYMBOL:
            x_wins(f'{BACKWARD_DIAGONAL}')
        elif BOARD_STATE[0][2] == O_SYMBOL:
            o_wins(f'{BACKWARD_DIAGONAL}')
        else:
            return False
        return True

    return False

def move_count() -> int:
    '''
    the number of moves that have been made so far

    Returns:
        the number of marks on the board (= number of moves)
    '''
    cnt = 0
    for row in BOARD_STATE:
        for cell in row:
            if cell in (X_SYMBOL, O_SYMBOL):
                cnt += 1
    return cnt

def make_mark(mark: str, x_coord: float, y_coord: float) -> None:
    '''
    draw an 'X' or 'O' in the cell which was clicked
    '''

    if is_out_of_bounds(x_coord, y_coord) or cell_is_occupied(x_coord, y_coord):
        # draw nothing
        return

    move_to_cell_bottom_center(STUDENT_TURTLE, x_coord, y_coord)

    if mark == X_SYMBOL:
        make_an_x(STUDENT_TURTLE, CELL_WIDTH)
    elif mark == O_SYMBOL:
        make_an_o(STUDENT_TURTLE, CELL_WIDTH)
    else:
        raise ValueError(f'invalid mark: {mark}')

    BOARD_STATE[2 - get_row(y_coord)][get_column(x_coord)] = mark
    if mark == X_SYMBOL:
        SCREEN.onscreenclick(draw_o)
    elif mark == O_SYMBOL:
        SCREEN.onscreenclick(draw_x)

    game_over = False
    if move_count() >= 5:
        game_over = check_for_win()

    if not game_over and move_count() == 9:
        game_over = True
        cat_wins()

    if game_over:
        STUDENT_TURTLE.penup()
        STUDENT_TURTLE.goto(0, 0)
        STUDENT_TURTLE.setheading(90)
        answer = prompt_for_new_game(SCREEN, STUDENT_TURTLE, CELL_WIDTH)
        if answer == 'yes':
            # reset turtles
            TURTLE.reset()
            STUDENT_TURTLE.reset()
            TURTLE.speed(0)
            STUDENT_TURTLE.speed(TURTLE_SPEED)

            # reset board
            for row in BOARD_STATE:
                row[:] = [' ', ' ', ' ']

            # restart game
            draw_board()
            SCREEN.onscreenclick(draw_x)
        else:
            SCREEN.bye()



def draw_x(x_coord: float, y_coord: float) -> None:
    '''
    draw an 'X' in the cell which was clicked
    '''
    make_mark(X_SYMBOL, x_coord, y_coord)

def draw_o(x_coord: float, y_coord: float) -> None:
    '''
    draw an 'X' in the cell which was clicked
    '''
    make_mark(O_SYMBOL, x_coord, y_coord)

def start() -> None:
    '''
    start the game
    '''
    draw_board()
    SCREEN.onscreenclick(draw_x)
    done()

if __name__ == '__main__':

    # you can change these values
    CELL_WIDTH = 100  # pixels
    TURTLE_SPEED = 0

    ########################################
    # DO NOT CHANGE THESE VALUES
    # you can, but there's no reason to
    ########################################

    # the internal representation of the state of the game board
    BOARD_STATE = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
        ]

    # a turtle to use for utility drawing
    TURTLE = Turtle()
    TURTLE.speed(0)

    # a turtle for the student to use (and not affect the utility turtle)
    STUDENT_TURTLE = Turtle()
    STUDENT_TURTLE.speed(TURTLE_SPEED)

    # the screen object
    SCREEN = Screen()
    SCREEN.setup(5*CELL_WIDTH, 5*CELL_WIDTH)

    # constants to make the code more readable
    X_SYMBOL = 'x'
    O_SYMBOL = 'o'
    ROW = 'r'
    COLUMN = 'c'
    DIAGONAL = 'd'
    FORWARD_DIAGONAL = 'd1'
    BACKWARD_DIAGONAL = 'd2'
    BOARD_WIDTH = 3 * CELL_WIDTH  # pixels
    LEFT = BOTTOM = int(-3 * CELL_WIDTH / 2)  # pixel offset from (0,0)
    RIGHT = TOP = int(3 * CELL_WIDTH / 2)  # pixel offset from (0,0)

    start()
