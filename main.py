import util
import dictionaries
import engine
import ui
import time
import players
import menu_start
import view
from art import text2art
from termcolor import colored
from PIL import Image
from pygame import mixer
import data_manager

def main():
    MUSIC_FILE = "Cookie Monster Sings C is for Cookie.wav"
    mixer.init()
    mixer.music.load(MUSIC_FILE)
    mixer.music.play()
    view.print_images(data_manager.read_file_record('ascii-art.txt'))
    view.start_descriptions()    
    # initial level
    level = 'BOARD_1'   

    # initial key
    key = ''

    menu_start.run()
        
    ui.print_message('\n\n\n LEVEL %s \n\n\n' % (level[-1]))
    time.sleep(1.0)
    util.clear_screen()
    

    pass_key_input = False

    while level != 'WIN' and level != 'QUIT' and level != 'LOSE':
        
        util.clear_screen()
        pass_key_input = False
        
        view.print_table(players.data_to_print(dictionaries.player))
       
        # Set up board
        board = engine.create_board(dictionaries.BOARD[level])
        board = engine.put_other_on_board(board, dictionaries.others, level)
        board = engine.put_item_on_board(board, dictionaries.items, level) 
        board = engine.put_player_on_board(board, dictionaries.player)

        # Display essential info
        ui.print_player_essential_atributes(dictionaries.player)
        
        # Display board
        ui.display_board(board)

        # Message panel intoduction (always displayed)
        ui.print_message('  MESSAGE PANEL \n' + 17 * '-' + '\n')

        # Interaction whit items
        engine.item_vs_player(dictionaries.inventory, dictionaries.items, dictionaries.player, level, dictionaries.items)

        # Display inventory
        if key == 'i':
            ui.print_message('This is your inventory content: ')
            ui.print_table(dictionaries.inventory)

        # Display statistics
        if key == "p":
            engine.show_statistics(dictionaries.player)

        # Interaction with other characters
        if engine.player_meets_other(dictionaries.others, dictionaries.player, level, board) != False:
            other = engine.player_meets_other(dictionaries.others, dictionaries.player, level, board)
            if dictionaries.others[other]['other_type'] == 'enemy':
                engine.fight(dictionaries.player, dictionaries.others, other, dictionaries.inventory, dictionaries.items)
            elif dictionaries.others[other]['other_type'] == 'quiz':
                engine.player_vs_other_quiz(dictionaries.player, other, dictionaries.others, dictionaries.inventory, dictionaries.others[other]['questions'])

        # Insert secret code
        if key == "c":
            engine.use_secret_code(dictionaries.player, dictionaries.others, level, dictionaries.codes)

        # Gate and level change handling      
        if engine.player_enters_gate(level, dictionaries.BOARD, dictionaries.player, key, dictionaries.inventory, dictionaries.others) != level:
            util.clear_screen()
            level = engine.player_enters_gate(level, dictionaries.BOARD, dictionaries.player, key, dictionaries.inventory, dictionaries.others)

            if level == 'BOARD_2' or level == 'BOARD_3':
                dictionaries.player['position_y'] = 15
                dictionaries.player['position_x'] = 3
    
            if level == 'WIN':
                pass_key_input = True
                pass
            else:
                ui.print_message('\n\n\n LEVEL %s \n\n\n' % (level[-1]))
                time.sleep(1.0)
                util.clear_screen()
                pass_key_input = True
                
    
        # Player input
        if pass_key_input == False:
            key = util.key_pressed()

        # Movement
        if pass_key_input == False:
            engine.movement(board, dictionaries.player, key, dictionaries.others) 
   

        # Check if quit
        if key == 'q':
            quit_assertion = ''
            while quit_assertion != 'y' and quit_assertion != 'n':
                util.clear_screen()
                print('Are you sure you want to quit? ( Y / N )')
                quit_assertion = util.key_pressed()
                if quit_assertion == 'y':
                    level = 'QUIT'
                elif quit_assertion == 'n':
                    pass
                else:
                    pass




        if dictionaries.player['player_life'] == 0:
            level = 'LOSE'


    if level == 'WIN':
        util.clear_screen()
        ui.display_board(board)
        print(text2art("VICTORY!", font='block', chr_ignore=True))

    elif level == 'LOSE':
        util.clear_screen()
        ui.display_board(board)
        print(text2art("GAME OVER!", font='block', chr_ignore=True))

        time.sleep(10.7)
    
    ui.authors_presentation()
    players.add_results(players.count_points(), "results.txt")
    print('\n\n\n Goodbye, see you soon!')
    time.sleep(1.0)

    with Image.open("cookiemonster.jpg") as img:
        img.show()


if __name__ == '__main__':
    main()