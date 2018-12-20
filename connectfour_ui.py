#IDs: Jeremy Parnell(27005248) Jade Lam(49109437)
#connectfour_ui

import connectfour_sockets
import console_only
import connectfour


def _host_input():
    '''
    Prompts the user to enter in a host name. Returns the host name
    '''
    while True:
        host = input('Host: ').strip()
        if host == '':
            print('Please specify a host (either a name or an IP address)')
        else:
            return host


def _port_input():
    '''
    Prompts the user to enter in a port number. Catches any errors, such as the
    user entering an invalid port number
    '''
    while True:
        try:
            port = int(input('Port: ').strip())

            if port < 0 or port > 65535:
                print('Ports must be an integer between 0 and 65535')
            else:
                return port
        except ValueError:
            print('Ports must be an integer between 0 and 65535')


def _ask_for_username():
    '''
    Prompts the user to enter in a valid username. Catches any errors, such
    as the user entering a username with a space or tab, or the user entering
    an empty string 
    '''
    print("Please Enter In A Username. Username Must Not Contain Any Spaces Or Tabs")
    while True:
        username = input('Username: ')
        if len(username) > 0:
            if ' ' in username or '\t' in username:
                print("You may not have spaces in your username. Try again")
                continue
            else:
                 break
        else:
            print('That username is blank; please try again')
    print("_________________________________________________________________________")
    return username


def _establish_connection():
    '''
    Establishes connection with the server. If a connection has not been reached,
    the program will ask the user to reenter information until a connection is
    reached
    '''
    while True:
        try:
            host = _host_input()
            port = _port_input()
            print()
            print('Connecting to {} (port {})...'.format(host,port))
            connection = connectfour_sockets.connect(host,port)
            print('\nConnected!\n')
            return connection
        except:
            print("\nCould Not Connect. Please Try Again")
            continue


def _start_game(connection):
    '''
    Takes a connection as a parameter. This function establishes the connection
    and intiates the beginning to the connect four game, letting the player know
    they are the RED player
    '''
    username = _ask_for_username()
    connectfour_sockets.hello(connection, username)
    connectfour_sockets.initialize(connection)
    print("{}...you are the RED player!\n".format(username))

  
def _game():
    '''
    Runs the console-mode user interface from start to finish.
    '''
    try:
        connection = _establish_connection()
        _start_game(connection)
        gamestate = console_only.welcome()
        while True:
            try:
                player = console_only.move(gamestate)
                col = console_only.get_column()
                gamestate = console_only.user_input(gamestate, player, col)
                if player.strip().upper() == "DROP":
                    gamestate = connectfour_sockets.send_drop(gamestate,connection,col)
                elif player.strip().upper() == "POP":
                    gamestate =connectfour_sockets.send_pop(gamestate,connection,col)
                if connectfour.winner(gamestate) != 0:
                    console_only.win(gamestate)
                    break
            except:
                continue
    except:
        print("\nInvalid Request Was Given")
        pass
    
    finally:
        connectfour_sockets.close(connection)


if __name__== "__main__":
    _game()
