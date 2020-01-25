import data_manager
import view
import sys
import main
import dictionaries
from termcolor import colored

BOARD_WIDTH = 80
BOARD_HEIGHT = 20

file_nicknames = "data_nickname.txt"
file_results = "results.txt"


list_labels = ["Nickname", "Type", "Level of difficulty"]

game_player = {'race' : ['1', '2', '3'],
            'Level_of_difficulty' : ['1', '2', '3'],
}

def user_info(list_labels, player_nickname):

    print("Please, provide your's nickname: ")

    nickname = 0
    for elem in range(len(list_labels)):
        user_answer = input(str(list_labels[elem])+" : ")
        if elem == 0:
            data_manager.read_file_nicknames(file_nicknames)
            for line in player_nickname:
                if user_answer == line:
                    raise Exception("This user already exist. Try again and select other name")
            print("\nYou can choose who you want to be :D \nYour options: (1)CookieMan, (2)CookieMum or (3)CookieBaby\n")        
        
        elif elem == 1:
            if user_answer not in game_player['race']:
                raise Exception(colored("It's not acceptable choice. Try again\n", "red"))   
            else:
                if user_answer == '1':
                    print("You are a CookieMan so you are more powerful than you think")
                    dictionaries.player['player_power'] = 5
                elif user_answer == '2':
                    print("You chose CookieMum and you get rolling pin :D!!!It can be useful later")
                    dictionaries.player['additional_elements'] = 'rolling_pin'
                elif user_answer == '3':    
                    print("Hello little boy ;) Because you're still a child, You get a more life_points ")
                    dictionaries.player['player_life'] = 2
        
        elif elem == 2:
            if user_answer not in game_player['Level_of_difficulty']:
                raise Exception(colored("You choose only 1 ,2 or 3 level of difficulty\n", "red"))
            else:
                if user_answer == '1':
                    dictionaries.player['player_life'] = dictionaries.player['player_life'] + 5
                elif user_answer == '2':
                    dictionaries.player['player_life'] = dictionaries.player['player_life'] + 3
                elif user_answer == '3':
                    dictionaries.player['player_life'] = dictionaries.player['player_life'] + 1
     
        dictionaries.player[list_labels[elem]] = user_answer
    data_manager.add_new_nicknames(dictionaries.player, file_nicknames)    
    



def data_to_print(data):
    keys = ["Nickname", "Type", "Level of difficulty"]
    data_print = {key : dictionaries.player[key] for key in keys }
    return data_print
