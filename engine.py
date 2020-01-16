import random


def create_board(width, height):
    '''
    Creates a new game board based on input parameters.

    Args:
    int: The width of the board
    int: The height of the board

    Returns:
    list: Game board
    '''

    board = []

    board.append([''] + width * ['-'])

    for a in range(height - 2):
        board.append(['|'] + (width - 2) * [' '] + ['|'])

    board.append([''] + width * ['-'])

    return board


def put_player_on_board(board, player):
    '''
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    '''
    x = 0
    for row in board:
        y = 0
        for cell in row:
            if cell == player['player_icon']:
                board[x][y] = ' '
            y += 1
        x += 1

    height = player['position_y'] - 1
    width = player['position_x'] - 1
    board[height][width] = player['player_icon']

    return board


def put_other_on_board(board, other):
    '''
    Modifies the game board by placing the other character icon at its coordinates.

    Args:
    list: The game board
    dictionary: The other character information containing the icon and coordinates

    Returns:
    Nothing
    '''

    x = 0
    for row in board:
        y = 0
        for cell in row:
            if cell == other["other_icon"]:
                board[x][y] = ' '
            y += 1
        x += 1

    # for line in board:
    #     for cell in line:
    #         if cell == other["other_icon"]:
    #             cell = " "

    x_index = other["position_x"]
    y_index = other["position_y"]
    board[x_index][y_index] = other["other_icon"]

    return board


def get_random_position_of_other(other):
    random_selection = random.randrange(4)
    if random_selection == 0:
        other["position_x"] += other["step"]
    elif random_selection == 1:
        other["position_x"] -= other["step"]
    elif random_selection == 2:
        other["position_y"] += other["step"]
    elif random_selection == 3:
        other["position_y"] -= other["step"]
