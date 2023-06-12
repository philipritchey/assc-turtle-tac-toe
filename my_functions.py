'''
functions that the student should implement
'''

def make_an_x(turtle, cell_width: int) -> None:
    '''
    draw an 'X' above where the turtle is.

    Args:
        turtle: the turtle to use for drawing.
        cell_width: width of a game board cell in pixels.
    '''

    # when this function is called the turtle is
    #   * at the bottom center of the cell
    #   * facing north
    #   * pen up
    # +---+
    # |   |
    # +-^-+

    #
    # TODO(student): draw an 'X' symbol
    #
    # this is the "lame" way: write text 'X'
    #   you must replace this with your own, not lame, X
    turtle.write('X', align='center', font=('Arial', int(3*cell_width/4), 'normal'))


def make_an_o(turtle, cell_width: int) -> None:
    '''
    draw an 'O' above where the turtle is.

    Args:
        turtle: the turtle to use for drawing.
        cell_width: width of a game board cell in pixels.
    '''

    # when this function is called the turtle is
    #   * at the bottom center of the cell
    #   * facing north
    #   * pen up
    # +---+
    # |   |
    # +-^-+

    #
    # TODO(student): draw an 'O' symbol
    #
    # this is the "lame" way: write text 'O'
    #   you must replace this with your own, not lame, O
    turtle.write('O', align='center', font=('Arial', int(3*cell_width/4), 'normal'))

def make_a_cat(turtle, cell_width: int) -> None:
    '''
    draw a "cat" over the game board.

    Args:
        turtle: the turtle to use for drawing.
        cell_width: width of a game board cell in pixels.
    '''

    # when this function is called the turtle is
    #   * at the origin, (0, 0)
    #   * facing north
    #   * pen up
    #  | |
    # -+-+-
    #  |^|
    # -+-+-
    #  | |

    #
    # TODO(student): draw a symbol/sign representing the cat's game (a game ending in a tie)
    #
    # this is the "lame" way: write text 'C'
    #   you must replace this with your own, not lame, cat symbol
    turtle.back(cell_width * 1.5)
    turtle.pencolor('blue')
    turtle.write('C', align='center', font=('Arial', int(2*cell_width), 'normal'))

def announce_winner_is_x(turtle, cell_width: int) -> None:
    '''
    announce that X wins

    Args:
        turtle: the turtle to use for drawing.
        cell_width: width of a game board cell in pixels.
    '''

    # when this function is called the turtle is
    #   * at the origin, (0, 0)
    #   * facing north
    #   * pen up
    #  | |
    # -+-+-
    #  |^|
    # -+-+-
    #  | |

    #
    # TODO(student): draw something to say that X wins
    #
    # this is the "lame" way: write text 'X wins'
    #   you must replace this with your own, not lame, drawing
    turtle.forward(cell_width * 1.5)
    turtle.pencolor('red')
    turtle.write('X wins', align='center', font=('Arial', int(cell_width), 'normal'))

def announce_winner_is_o(turtle, cell_width: int) -> None:
    '''
    announce that O wins

    Args:
        turtle: the turtle to use for drawing.
        cell_width: width of a game board cell in pixels.
    '''

    # when this function is called the turtle is
    #   * at the origin, (0, 0)
    #   * facing north
    #   * pen up
    #  | |
    # -+-+-
    #  |^|
    # -+-+-
    #  | |

    #
    # TODO(student): draw something to say that O wins
    #
    # this is the "lame" way: write text 'O wins'
    #   you must replace this with your own, not lame, drawing
    turtle.forward(cell_width * 1.5)
    turtle.pencolor('green')
    turtle.write('O wins', align='center', font=('Arial', int(cell_width), 'normal'))

def prompt_for_new_game(screen, turtle, cell_width: int) -> str:
    '''
    ask the user if they want to play again

    Args:
        screen: the graphics window
        turtle: the turtle to use for drawing.
        cell_width: width of a game board cell in pixels.

    Returns:
        'yes' if player wants a new game
        'no' (or anything except 'yes') if player wants to quit
    '''

    # when this function is called the turtle is
    #   * at the origin, (0, 0)
    #   * facing north
    #   * pen up
    #  | |
    # -+-+-
    #  |^|
    # -+-+-
    #  | |

    #
    # TODO(student): find out if the user wants to play again
    #
    # this is a partial solution, you must finish it or replace it
    answer = screen.textinput('title', 'prompt')
    return answer
