import random
import ui


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

    height = player['position_y']
    width = player['position_x']
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
            if cell == other['other_icon']:
                board[x][y] = ' '
            y += 1
        x += 1

    height = other['position_y']
    width = other['position_x']
    board[height][width] = other['other_icon']

    return board


def get_random_position_of_other(other, width, height):
    """
    Randomly generates and updates position of Other Character
    based on the Character's step. Other Character respects the walls.

    Args:
        other: dictionary
        BOARD_HEIGHT and BOARD_WEIGHT: int

    """
    if other["other_health"] > 0:
        random_selection = random.randrange(4)
        if random_selection == 0:
            potential_position = other["position_x"] + other["step"]
            if potential_position >= width - 1:
                pass
            else:
                other["position_x"] += other["step"]
        if random_selection == 1:
            potential_position = other["position_x"] - other["step"]
            if potential_position <= 0:
                pass
            else:
                other["position_x"] -= other["step"]
        if random_selection == 2:
            potential_position = other["position_y"] + other["step"]
            if potential_position >= height - 1:
                pass
            else:
                other["position_y"] += other["step"]
        if random_selection == 3:
            potential_position = other["position_y"] - other["step"]
            if potential_position <= 0:
                pass
            else:
                other["position_y"] -= other["step"]


def add_to_inventory(inventory, item_key):
    """Add to the inventory dictionary a list of items"""

    item_key = item_key[:-1]

    if item_key in inventory:
        inventory[item_key] += 1
    else:
        inventory[item_key] = 1


def put_item_on_board(board, item, item_key):

    board[item[item_key]['position_y']][item[item_key]['position_x']] = item[item_key]['item_icon']

    return board


def player_meets_other(other, player):
    """
    Checks if Player meets the Other Character (is next to it, above or under)
    Args:
        other: dictionary
        player: dictionary
    Returns:
        if_meet: boolean
    """
    if_meet = False
    if other["other_health"] > 0:
        if other["position_y"] == player["position_y"] and (other["position_x"] == player["position_x"] + 1 or other["position_x"] == player["position_x"] - 1):
            if_meet = True
        elif other["position_x"] == player["position_x"] and (other["position_y"] == player["position_y"] + 1 or other["position_y"] == player["position_y"] - 1):
            if_meet = True
        elif other["position_y"] == player["position_y"] and other["position_x"] == player["position_x"]:
            if_meet = True

    return if_meet


def movement(board, player, key, other, width, height):
    if key == 'w':
        if player['position_y'] == 1:
            pass
        else:
            player['position_y'] -= 1
        get_random_position_of_other(other, width, height)

    elif key == 's':
        if player['position_y'] == len(board) - 2:
            pass
        else:
            player['position_y'] += 1
        get_random_position_of_other(other, width, height)
    elif key == 'a':
        if player['position_x'] == 1:
            pass
        else:
            player['position_x'] -= 1
        get_random_position_of_other(other, width, height)
    elif key == 'd':
        if player['position_x'] == len(board[0]) - 3:
            pass
        else:
            player['position_x'] += 1
        get_random_position_of_other(other, width, height)
    else:
        pass


def item_vs_player(inventory, item, player):

    item_to_delete = ''

    for item_key in item:
        if item[item_key]['position_x'] == player['position_x'] and item[item_key]['position_y'] == player['position_y']:
            add_to_inventory(inventory, item_key)
            item_to_delete = item_key
            item[item_key]['number'] -= 1
            ui.print_message('This item has been added to your inventory!')

    if item_to_delete == '':
        pass

    elif item[item_to_delete]['number'] == 0:
        del item[item_to_delete]


def player_vs_other_quiz(player, other, item, questions_number=3):
    """
    Player fights agains the Other Character answering questions.
    When Player replies correctly, the Other Character loses health points.
    Otherwise Player loses health points.
    Player losing heath - game over. The Other Character losing
    health - it disappears and the Player gets flour.
    """
    question_prompts = [
        "What's the first name of 'Ooops I did it again' singer?\n(a) Christina\n(b) Britney\n(c) Jessica\n",
        "Which river passes through Vienna?\n(a) Vistula\n(b) Douro\n(c) Danube\n",
        "What color are bananas?\n(a) Red\n(b) Orange\n(c) Yellow\n",
        "What band Nergal plays in?\n(a) Behemoth\n(b) Acid Drinkers\n(c) Coma\n"
        ]

    questions = [
        [question_prompts[0], "b", False],
        [question_prompts[1], "c", False],
        [question_prompts[2], "c", False],
        [question_prompts[3], "a", False]
    ]

    print("Play the quiz to get flower from the Miller")
    q_count = 0
    while q_count <= questions_number and other["other_health"] > 0 and questions[q_count][2] is False:
        answer = input(questions[q_count][0])
        if answer == questions[q_count][1]:
            player["player_health"] += 1
            other["other_health"] -= 1
            questions[q_count][2] = True
            print("Correct!")
        else:
            player["player_health"] -= 1
            print("Wrong!")
        q_count += 1

    if other["other_health"] > 0:
        print("To get flour you have to come back and reply correctly to the questions!")
    else:
        item["flour0"]["number"] += 1
        print("Wonderful! The Miller gave you flour.")
