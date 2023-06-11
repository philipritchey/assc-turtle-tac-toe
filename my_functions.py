'''
functions that the student must implement
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
    #   you must replace this with you own, not lame, X
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
    #   you must replace this with you own, not lame, O
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
    # +---+
    # |   |
    # +-^-+

    #
    # TODO(student): draw a symbol/sign representing the cat's game (a game ending in a tie)
    #
    # this is the "lame" way: write text 'C'
    #   you must replace this with you own, not lame, cat symbol
    turtle.back(cell_width * 1.5)
    turtle.pencolor('blue')
    turtle.write('C', align='center', font=('Arial', int(2*cell_width), 'normal'))