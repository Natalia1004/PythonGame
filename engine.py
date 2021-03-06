import random
import ui
import main
import dictionaries
import math
import util
import view
import players


def create_board(board):

    brick = board['BRICK']
    width = board['WIDTH']
    height = board['HEIGHT']

    new_board = []

    new_board.append(width * [brick])

    for a in range(height - 2):
        new_board.append([brick] + (width - 2) * ['  '] + [brick])

    new_board.append(width * [brick])

    if board['GATES']['GATE_UP']['GATE_POSITION_Y'] == None:
        pass
    else:

        new_board[board['GATES']['GATE_UP']['GATE_POSITION_Y']][board['GATES']['GATE_UP']['GATE_POSITION_X']] = '  '

    if board['GATES']['GATE_DOWN']['GATE_POSITION_Y'] == None:
        pass
    else:

        new_board[board['GATES']['GATE_DOWN']['GATE_POSITION_Y']][board['GATES']['GATE_DOWN']['GATE_POSITION_X']] = '  '

    return new_board


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


def put_other_on_board(board, others, level):
    '''
    Modifies the game board by placing the other character icon at its coordinates.
    Args:
    list: The game board
    dictionary: The other character information containing the icon and coordinates
    Returns:
    Nothing
    '''
    
    for other in others:
        x = 0
        for row in board:
            y = 0
            for cell in row:
                if cell == others[other]['other_icon']:
                    board[x][y] = ' '
                y += 1
            x += 1

    for other in others:
        if others[other]["board"] == int(level[-1]) and others[other]['other_health'] >= 1:
            height = others[other]['position_y']
            width = others[other]['position_x']

            for row in range(height - (math.floor(others[other]["width"] / 2)), height + (math.ceil(others[other]["width"] / 2))):
                for cell in range(width - (math.floor(others[other]["width"] / 2)), width + (math.ceil(others[other]["width"] / 2))):
                    board[row][cell] = others[other]['other_icon']

    return board


def get_random_position_of_other(others, width, height):
    """
    Randomly generates and updates position of Other Character
    based on the Character's step. Other Character respects the walls.

    Args:
        other: dictionary
        BOARD_HEIGHT and BOARD_WEIGHT: int

    """
    for other in others:
        if other != "boss":
            if others[other]["other_health"] > 0:
                random_selection = random.randrange(4)
                # Going right
                if random_selection == 0:
                    potential_position = others[other]["position_x"] + others[other]["step"]
                    if potential_position >= width - 1:
                        pass
                    else:
                        others[other]["position_x"] += others[other]["step"]
                # Going left
                if random_selection == 1:
                    potential_position = others[other]["position_x"] - others[other]["step"]
                    if potential_position <= 0:
                        pass
                    else:
                        others[other]["position_x"] -= others[other]["step"]
                # Going down
                if random_selection == 2:
                    potential_position = others[other]["position_y"] + others[other]["step"]
                    if potential_position >= height - 1:
                        pass
                    else:
                        others[other]["position_y"] += others[other]["step"]
                # Going up
                if random_selection == 3:
                    potential_position = others[other]["position_y"] - others[other]["step"]
                    if potential_position <= 0:
                        pass
                    else:
                        others[other]["position_y"] -= others[other]["step"]
        elif other == 'boss':
            if others[other]["other_health"] > 0:
                random_selection = random.randrange(4)
                # Going right
                if random_selection == 0:
                    potential_position = others[other]["position_x"] + others[other]["step"]
                    if potential_position + 2 >= width - 1:
                        pass
                    else:
                        others[other]["position_x"] += others[other]["step"]
                # Going left
                if random_selection == 1:
                    potential_position = others[other]["position_x"] - others[other]["step"]
                    if potential_position - 2 <= 0:
                        pass
                    else:
                        others[other]["position_x"] -= others[other]["step"]
                # Going down
                if random_selection == 2:
                    potential_position = others[other]["position_y"] + others[other]["step"]
                    if potential_position + 2 >= height - 1:
                        pass
                    else:
                        others[other]["position_y"] += others[other]["step"]
                # Going up
                if random_selection == 3:
                    potential_position = others[other]["position_y"] - others[other]["step"]
                    if potential_position - 2 <= 0:
                        pass
                    else:
                        others[other]["position_y"] -= others[other]["step"]

                


def add_to_inventory(inventory, item_key):
    """Add to the inventory dictionary a list of items"""


    if item_key == 'first_aid':
        pass

    elif item_key in inventory:
        inventory[item_key] += 1
    else:
        inventory[item_key] = 1


def put_item_on_board(board, items, level):

    for item_key in items:
        if items[item_key]['board'] == int(level[-1]):
            board[items[item_key]['position_y']][items[item_key]['position_x']] = items[item_key]['item_icon']
        else:
            pass

    return board


def player_meets_other(others, player, level, board = ''):
    """
    Checks if Player meets the Other Character (is next to it, above or under)
    Args:
        other: dictionary
        player: dictionary
    Returns:
        if_meet: boolean
    """
    if_meet = False

    for other in others:
        if others[other]['board'] == int(level[-1]):
            if others[other]['other_name'] != 'Boss':
                if others[other]["other_health"] > 0:
                    if others[other]["position_y"] == player["position_y"] and (others[other]["position_x"] == player["position_x"] + 1 or others[other]["position_x"] == player["position_x"] - 1):
                        return other
                    elif others[other]["position_x"] == player["position_x"] and (others[other]["position_y"] == player["position_y"] + 1 or others[other]["position_y"] == player["position_y"] - 1):
                        return other
                    elif others[other]["position_y"] == player["position_y"] and others[other]["position_x"] == player["position_x"]:
                        return other
            elif others[other]['other_name'] == 'Boss':
                if board[(player["position_y"] + 1)][player["position_x"]] == '🍔' or board[(player["position_y"] - 1)][player["position_x"]] == '🍔':
                    return other
                elif board[player["position_y"]][(player["position_x"] + 1)] == '🍔' or board[player["position_y"]][(player["position_x"] - 1)] == '🍔':
                    return other

    return if_meet


def movement(board, player, key, others):

    height = len(board)
    width = len(board[0])
    if key in ['w', 's', 'a', 'd']:
        get_random_position_of_other(others, width, height)

    if key == 'w':
        if player['position_y'] == 1:
            pass
        else:
            player['position_y'] -= 1

    elif key == 's':
        if player['position_y'] == len(board) - 2:
            pass
        else:
            player['position_y'] += 1

    elif key == 'a':
        if player['position_x'] == 1:
            pass
        else:
            player['position_x'] -= 1

    elif key == 'd':
        if player['position_x'] == len(board[0]) - 2:
            pass
        else:
            player['position_x'] += 1

    else:
        pass


def item_vs_player(inventory, item, player, level, items):

    item_to_delete = ''

    for item_key in item:
        if item[item_key]['position_x'] == player['position_x'] and item[item_key]['position_y'] == player['position_y'] and items[item_key]['board'] == int(level[-1]):

            add_to_inventory(inventory, item_key)
            item_to_delete = item_key
            item[item_key]['number'] -= 1
            

            if item_key == 'first_aid':
                ui.print_message('\n' + ' +1 Life point! ')
                player['player_life'] += 1 
            else:
                ui.print_message('\n' + item_key + ' has been added to your inventory!')
                

    if item_to_delete == '':
        pass

    elif item[item_to_delete]['number'] == 0:
        item[item_to_delete]['board'] = -1

def add_life_points(item, player):

    try:

        if item['first_aid']['position_x'] == player['position_x'] and item['first_aid']['position_y'] == player['position_y']:
            player['player_life'] += 1
        
    except KeyError:
        pass
    
def player_enters_gate(level, BOARD, player, key, inventory, others):
    BOARD_level = BOARD[level]
   

    for board_ in BOARD:
        if board_ == level:
            for key_ in BOARD[board_]:
                if key_ == 'GATES':
                    for gate_ in BOARD[board_][key_]:
                        
                        # entering gate that is up in relation to player
                        if (player['position_y'] - 1) == BOARD[board_][key_][gate_]['GATE_POSITION_Y'] and (player['position_x']) == BOARD[board_][key_][gate_]['GATE_POSITION_X'] and key == 'w':
                            if gate_ == 'GATE_UP':
                                # Gate Requirements
                                if level == 'BOARD_1':
                                    if 'Donut' in inventory: #and others['other']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    else:
                                        ui.print_message('Come back with Donut!!')
                                elif level == 'BOARD_2':
                                    if 'Pralines' in inventory and others['other3']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    elif 'Pralines' in inventory   and others['other3']['other_health'] > 0:
                                        ui.print_message('Come back once you defeat the Cow!!')
                                    elif 'Pralines' not in inventory and others['other3']['other_health'] > 0:
                                        ui.print_message("Once you defeat Cow, come back with Pralines!")
                                    elif 'Pralines' not in inventory  and others['other3']['other_health'] == 0:
                                        ui.print_message("Come back with Pralines!")                                        
                                elif level == 'BOARD_3':
                                    if 'boss' not in others:
                                        return BOARD_level['NEXT_LEVEL']
                                    elif others['boss']['other_health'] > 0:
                                        ui.print_message('Come back once you defeat the Boss!!')
                            elif gate_ == 'GATE_DOWN':
                                return BOARD_level['PREVIOUS_LEVEL']                          

                        # entering gate that is down in relation to player
                        elif (player['position_y'] + 1 ) == BOARD[board_][key_][gate_]['GATE_POSITION_Y'] and (player['position_x']) == BOARD[board_][key_][gate_]['GATE_POSITION_X'] and key == 's':
                            if gate_ == 'GATE_UP':
                                # Gate Requirements
                                if level == 'BOARD_1':
                                    if 'Donut' in inventory: #and others['other']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    else:
                                        ui.print_message('Come back with Donut!!')
                                elif level == 'BOARD_2':
                                    if 'Pralines' in inventory and others['other3']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    elif 'Pralines' in inventory   and others['other3']['other_health'] > 0:
                                        ui.print_message('Come back once you defeat the Cow!!')
                                    elif 'Pralines' not in inventory and others['other3']['other_health'] > 0:
                                        ui.print_message("Once you defeat Cow, come back with Pralines!")
                                    elif 'Pralines' not in inventory  and others['other3']['other_health'] == 0:
                                        ui.print_message("Come back with Pralines!")                                        
                                elif level == 'BOARD_3':
                                    if others['boss']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    elif others['boss']['other_health'] > 0:
                                        ui.print_message('Come back once you defeat the Boss!!')
                            elif gate_ == 'GATE_DOWN':
                                return BOARD_level['PREVIOUS_LEVEL'] 

                        # entering gate that is left in relation to player
                        elif (player['position_x'] - 1) == BOARD[board_][key_][gate_]['GATE_POSITION_X'] and player['position_y'] == BOARD[board_][key_][gate_]['GATE_POSITION_Y'] and key == 'a':
                            if gate_ == 'GATE_UP':
                                # Gate Requirements
                                if level == 'BOARD_1':
                                    if 'Donut' in inventory: #and others['other']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    else:
                                        ui.print_message('Come back with Donut!!')
                                elif level == 'BOARD_2':
                                    if 'Pralines' in inventory and others['other3']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    elif 'Pralines' in inventory   and others['other3']['other_health'] > 0:
                                        ui.print_message('Come back once you defeat the Cow!!')
                                    elif 'Pralines' not in inventory and others['other3']['other_health'] > 0:
                                        ui.print_message("Once you defeat Cow, come back with Pralines!")
                                    elif 'Pralines' not in inventory  and others['other3']['other_health'] == 0:
                                        ui.print_message("Come back with Pralines!")                                        
                                elif level == 'BOARD_3':
                                    if others['boss']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    elif others['boss']['other_health'] > 0:
                                        ui.print_message('Come back once you defeat the Boss!!')
                            elif gate_ == 'GATE_DOWN':
                                return BOARD_level['PREVIOUS_LEVEL'] 

                        # entering gate that is right in relation to player
                        elif (player['position_x'] + 1) == BOARD[board_][key_][gate_]['GATE_POSITION_X'] and player['position_y'] == BOARD[board_][key_][gate_]['GATE_POSITION_Y'] and key == 'd':
                            if gate_ == 'GATE_UP':
                                # Gate Requirements
                                if level == 'BOARD_1':
                                    if 'Donut' in inventory: #and others['other']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    else:
                                        ui.print_message('Come back with Donut!!')
                                elif level == 'BOARD_2':
                                    if 'Pralines' in inventory and others['other3']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    elif 'Pralines' in inventory   and others['other3']['other_health'] > 0:
                                        ui.print_message('Come back once you defeat the Cow!!')
                                    elif 'Pralines' not in inventory and others['other3']['other_health'] > 0:
                                        ui.print_message("Once you defeat Cow, come back with Pralines!")
                                    elif 'Pralines' not in inventory  and others['other3']['other_health'] == 0:
                                        ui.print_message("Come back with Pralines!")                                        
                                elif level == 'BOARD_3':
                                    if others['boss']['other_health'] == 0:
                                        return BOARD_level['NEXT_LEVEL']
                                    elif others['boss']['other_health'] > 0:
                                        ui.print_message('Come back once you defeat the Boss!!')
                            elif gate_ == 'GATE_DOWN':
                                return BOARD_level['PREVIOUS_LEVEL'] 
    return level

def gate_requirements(level, inventory, others, gate_, BOARD_level):
    # Gate Requirements
    if level == 'BOARD_1':
        if 'Candy' in inventory and others['other']['other_health'] == 0:
            return BOARD_level['NEXT_LEVEL']
        
    elif level == 'BOARD_2':
        if 'Candy' in inventory and others['other3']['other_health'] == 0:
            return BOARD_level['NEXT_LEVEL']
    elif level == 'BOARD_3':
        if others['Boss']['other_health'] == 0:
            return BOARD_level['NEXT_LEVEL']
    elif gate_ =='GATE_DOWN':
        return BOARD_level['PREVIOUS_LEVEL'] 
        
        


def player_vs_other_quiz(player, other, others, inventory, questions, questions_number=2):
    """
    Player fights agains the Other Character answering questions.
    When Player replies correctly, the Other Character loses health points.
    Otherwise Player loses health points.
    Player lost all health - game over. The Other Character losing
    health - it disappears and the Player gets flour.
    """

    ui.print_message(("Play the quiz to get %s from the %s" % (others[other]["goal_quiz"], others[other]["other_name"])))

    q_count = 0

    questions = [question for question in questions if question[2] is False]

    while q_count <= questions_number and others[other]["other_health"] > 0:
        answer = input(questions[q_count][0])
        if answer == questions[q_count][1]:
            others[other]["other_health"] -= 1
            questions[q_count][2] = True
            ui.print_message("Correct!")
        else:
            ui.print_message("Wrong!")
        q_count += 1

    if others[other]["other_health"] > 0:
        player["player_life"] -= 1
        player['loss'] += 1
        ui.print_message("To get %s you have to come back and reply correctly to the questions!" % others[other]["goal_quiz"])
    else:
        player["player_life"] += 1
        player['wins'] += 1
        add_to_inventory(inventory, "Jelly")
        ui.print_message("Wonderful! The %s gave you %s." % (others[other]["other_name"], others[other]["goal_quiz"]))
        ui.print_message('+1 life point!')




def fight(player, others, other, inventory, items):
    
    player_x = player['position_x']
    player_y = player['position_y']
    other_x = others[other]['position_x']
    other_y = others[other]['position_y']

    items_summaric_power = 0
    items_summaric_protection = 0
    if player_x == other_x and player_y == other_y:
        for item in inventory:
            items_summaric_power += items[item]['added_power']
            items_summaric_protection += items[item]['added_protection']

    player_hit = (player['player_power'] + items_summaric_power) * random.randrange(5)
    other_hit = (others[other]['other_power'] - items_summaric_protection) * random.randrange(5)

    if player_hit > other_hit:
        ui.print_message('You just won the fight with %s! +1 to power for you!' %(others[other]['other_name']))
        player['player_power'] += 1
        player['wins'] += 1
        others[other]['other_health'] -= 1

    elif player_hit == other_hit:
        ui.print_message('You just fought with %s! It was a draw' %(others[other]['other_name']))
    
    else:
        ui.print_message('You just lost fight with %s! You loose one life point' %(others[other]['other_name']))
        player['player_life'] -= 1
        player['loss'] += 1


def add_secret_code(codes):
    added_code = input("Insert the code: ")
    if added_code not in codes.values():
        raise TypeError("Code incorrect")
    return added_code


def use_secret_code(player, others, level, codes):
    try:
        added_code = add_secret_code(codes)
    except TypeError as err:
        print(err)
    else:
        if added_code == codes["kill_others"]:
            for other in others:
                others[other]['other_health'] = 0
        elif added_code == codes["extra_lives"]:
            player['player_life'] += 3
        player['used_code'] = True


def show_statistics(player):
    statistics_keys = ("wins", "loss", 'discovered_boards')
    statistics_dict = {}
    for k in player:
        if k in statistics_keys:
            statistics_dict[k] = player[k]
    ui.print_table(statistics_dict)
