#IDs: Jeremy Parnell(27005248) Jade Lam(49109437)
#connectfour_socket

from collections import namedtuple
import socket
import console_only

Con4Connection = namedtuple(
    'Con4Connection',
    ['socket', 'inpt', 'output'])


class ConnectFourError(Exception):
    pass


_SHOW_DEBUG_TRACE = False


def connect(host,port):
    '''
    Connects to a server running on the given host and listening
    on the given port, returning a Con4Connection object describing
    that connection if successful, or raising an exception if the attempt
    to connect fails.
    '''
    c4socket = socket.socket()   
    c4socket.connect((host, port))
    c4socket_input = c4socket.makefile('r')
    c4socket_output = c4socket.makefile('w')
    return Con4Connection(
        socket = c4socket,
        inpt = c4socket_input,
        output = c4socket_output)


def hello(connection: Con4Connection, username):
    '''
    Logs a user into the connect four service over a previously-made connection.
    If the attempt to send text to the connect four server or receive a response
    fails (or if the server sends back a response that does not conform to
    the connect four protocol), an exception is raised.
    '''
    _write_line(connection, 'I32CFSP_HELLO ' + username)
    response = _read_line(connection)
    if response.startswith('\nWELCOME '):
        print(response)
    else:
        pass


def initialize(connection: Con4Connection):
    '''
    Initializes the game with the AI
    '''
    _write_line(connection, "AI_GAME")
    response = _read_line(connection)
    if response == 'READY':
        print('\nGAME START:')
    else:
        raise ConnectFourError()


def send_drop(gamestate, connection: Con4Connection, column):
    '''
    This function takes a gamestate, a connection, and a column number and sends
    the users designated 'drop' move to the server. Then it receives a response
    from the server. If the server responds with a valid move, the function will
    return a gamestate with the AI's move recorded. Else if the response is invalid,
    the function will catch it and prompt the user again for inputs
    '''
    _write_line(connection, 'DROP {}'.format(column))
    while True:
        response = _read_line(connection)
        if len(response) > 0:
            if response == 'OKAY':
                pass
            elif response.startswith('DROP') or response.startswith('POP'):
                move = response.split()[0]
                col = int(response.split()[1])
                print("YELLOW PLAYER IS CHOOSING...")
                gamestate = console_only.user_input(gamestate, move, col)
            elif response == "READY" or response.startswith("WINNER"):
                return gamestate
            elif response == 'INVALID':
                continue
        else:
            break

       
def send_pop(gamestate, connection: Con4Connection, column):
    '''
    This function takes a gamestate, a connection, and a column number and sends
    the users designated 'pop' move to the server. Then it receives a response
    from the server. If the server responds with a valid move, the function will
    return a gamestate with the AI's move recorded. Else if the response is invalid,
    the function will catch it and prompt the user again for inputs
    '''
    _write_line(connection, 'POP {}'.format(column))
    while True:
        response = _read_line(connection)
        if len(response) > 0:
            if response == 'OKAY':
                pass
            elif response.startswith('DROP') or response.startswith('POP'):
                move = response.split()[0]
                col = int(response.split()[1])
                print("YELLOW PLAYER IS CHOOSING...")
                gamestate = console_only.user_input(gamestate, move, col)
            elif response == "READY" or response.startswith("WINNER"):
                return gamestate
            elif response == 'INVALID':
                continue
        else:
            return gamestate

    
def close(connection: Con4Connection):
    '''
    This function takes a connection as a paramter and closes all connection
    to the server
    '''
    connection.inpt.close()
    connection.output.close()
    connection.socket.close()
    print("\nClosing connection. Goodbye...")



#Private Functions
#___________________________________________________
    
def _read_line(connection: Con4Connection):
    '''
    Reads a line of text sent from the server and returns it without
    a newline on the end of it
    '''
    line = connection.inpt.readline()[:-1]
    if _SHOW_DEBUG_TRACE:
        print('RCVD: ' + line)

    return line


def _write_line(connection: Con4Connection,line):
    '''
    Writes a line of text to the server, including the appropriate
    newline sequence, and ensures that it is sent immediately.
    '''
    connection.output.write(line + '\r\n')
    connection.output.flush()

    if _SHOW_DEBUG_TRACE:
        print('SENT: ' + line)
