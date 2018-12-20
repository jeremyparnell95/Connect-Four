#IDs: Jeremy Parnell(27005248) Jade Lam(49109437)
#console_only

import connectfour

def welcome():
    '''
    Function displays welcome message, prints the empty board of the new game,
    and returns the first gamestate
    '''
    print("Welcome to ICS 32 Connect Four\n")
    _print_board(connectfour.new_game())
    print()
    return connectfour.new_game()


def move(gamestate):
    '''
    Takes in a gamestate as a parameter. Prints the current players turn and
    asks for a move, "DROP" or "POP", and returns the move. Catches any input
    errors such as entering a move that isn't one of the ones specified or entering
    an empty string
    '''
    _print_turn(gamestate)
    while True:
        move = input("Drop or Pop: ")
        if len(move) > 0:
            if move.strip().upper() == "DROP" or move.strip().upper() == "POP":
                return move
            else:
                print("\nPlease use viable move")
                continue
        else:
            print("\nPlease type in a move")
            continue
        break
    return move


def get_column():
    '''
    Asks the user for and returns column number. Catches if the user enters an
    invalid response or a number that isn't a column on the board
    '''
    while True:
        try:
            col = int(input("Choose a column number between 1-7: "))
            if col > 0 and col < 8:
                return col
            else:
                print("\nPlease choose a viable number")
                continue
        except:
            print("\nTry Again")
            continue


def drop(gamestate,col):
    '''
    Takes in a gamestate and an integer-column number as parameters. Returns a
    new gamestate with the designated column dropped with a game piece. Catches
    any invalid move errors, such as dropping into a column that is already filled
    '''
    while True:
        try:              
            print()
            _print_board(connectfour.drop(gamestate,col-1))
            print()
            break
        except connectfour.InvalidMoveError:
            print("You cannot DROP that spot. Please choose a new move\n")
            break
        except:
            print("\nTry Again")
            continue
    return connectfour.drop(gamestate,col-1)

   
def pop(gamestate,col):
    '''
    Takes in a gamestate and an integer-column number as parameters. Returns a
    new gamestate with the designated column popped a game piece. Catches
    any invalid move errors, such as popping an empty column or trying
    to pop a piece that isn't theirs
    '''
    while True:
        try:
            print()
            _print_board(connectfour.pop(gamestate,col-1))
            print()
            break
        except connectfour.InvalidMoveError:
            print("You cannot POP that spot. Please choose a new move\n")
            break
        except:
            print("\nTry Again")
            continue
    return connectfour.pop(gamestate,col-1)


def user_input(gamestate, player, col):
    '''
    Takes in a gamestate, a move, and a column number and returns a new gamestate
    after the player's choice has been entered in.
    '''
    if player.strip().upper() == "DROP":
        result = drop(gamestate,col)
        if result == 0:
            pass
    elif player.strip().upper() == "POP":
        result = pop(gamestate,col)
        if result == 0:
            pass
    return result


def win(gamestate):
    '''
    Takes in a winning gamestate as a paramter and prints out the winning message
    '''
    if connectfour.winner(gamestate) == 1:
        print("Red Player Wins!\n")
    elif connectfour.winner(gamestate) == 2:
        print("Yellow Player Wins!\n")
    print("GAME OVER")



#Private Functions
#___________________________________________________
    
def _print_board(gamestate):
    '''
    Takes in a gamestate and prints out the gameboard
    '''
    new = gamestate.board
    for x in range(1,connectfour.BOARD_COLUMNS+1):
        print(str(x), end = "  ")
    print()
    for x in range(0,connectfour.BOARD_ROWS):
        content=''
        for y in range(0,connectfour.BOARD_COLUMNS):
            if new[y][x] == 0:
                content+="."+"  "
            elif new[y][x] == 1:
                content+="R"+"  "
            elif new[y][x] == 2:
                content+="Y"+"  "
        print(content)

        
def _print_turn(gamestate):
    '''
    Takes in a gamestate as a parameter and prints out the current player's turn
    '''
    player = ' '
    if gamestate.turn == 1:
        player = 'RED'
    elif gamestate.turn == 2:
        player = 'YELLOW'
    print("It is {} player's turn".format(player))


def _gameplay():
    '''
    Runs the console-mode user interface from start to finish
    '''
    gamestate = welcome()
    while True:
        try:
            player = move(gamestate)
            col = get_column()
            gamestate = user_input(gamestate, player, col)
            if connectfour.winner(gamestate) != 0:
                win(gamestate)
                break
        except:
            pass

        
if __name__=='__main__':
    _gameplay()

    
        
        

       
    

    
        
        
    
    
        

