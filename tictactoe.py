import copy
import random
from time import sleep

player = 'X'
cpu = 'O'

board = [
        [' ',' ',' '],
        [' ',' ',' '],
        [' ',' ',' ']
]



def print_board(game_state):
    print('  0  1  2\n  -------')
    for row in range(3):
        print(f'{row} |', end='')
        for cell in range(3):
            print(f'{game_state[row][cell]}', end='|')
        print('\n  -------')

def find_empty(game_state):
    empty_cells = []
    for x in range(0,3):
        for y in range(0,3):
            if game_state[y][x] == ' ':
                empty_cells.append([y,x])
    return empty_cells


def minimax(game_state, depth, player_turn):

    result = win_game(game_state)

    if result is not None:
        if result == player:
            return -10
        elif result == cpu:
            return 10
        else:
            return 0
    else:
        empty_cells = find_empty(game_state)
        if player_turn == 'MAX':
            best_score = -float('inf')
            for cell in empty_cells:
                temp_board = copy.deepcopy(game_state)
                temp_board[cell[0]][cell[1]] = cpu
                best_score = max(best_score, minimax(temp_board, depth - 1, 'MIN'))
            return best_score
        else:
            best_score = float('inf')
            for cell in empty_cells:
                temp_board = copy.deepcopy(game_state)
                temp_board[cell[0]][cell[1]] = player
                best_score = min(best_score, minimax(temp_board, depth - 1, 'MAX'))
            return best_score

def get_best_move(game_state):
    empty_cells = find_empty(game_state)
    temp_board = copy.deepcopy(game_state)
    best_score = -float('inf')
    best_moves = []
    if len(empty_cells) == 0:
        return None
    else:
        for cell in empty_cells:
            temp_board[cell[0]][cell[1]] = cpu
            rec_score = minimax(temp_board, 5, 'MIN')
            if best_score < rec_score:
                best_score = rec_score
                best_moves = [cell]
            elif best_score == rec_score:
                best_moves.append(cell)
            temp_board = copy.deepcopy(game_state)
        return random.choice(best_moves)

def win_game(game_state):
    empty_cells = find_empty(game_state)
    for x in range(3):
        if game_state[0][x] == game_state[1][x] == game_state[2][x] != ' ':
            return game_state[0][x]
        elif game_state[x][0] == game_state[x][1] == game_state[x][2] != ' ':
            return game_state[x][0]

    if game_state[0][0] == game_state[1][1] == game_state[2][2] != ' ':
        return game_state[0][0]

    elif game_state[0][2] == game_state[1][1] == game_state[2][0] != ' ':
        return game_state[0][2]

    if len(empty_cells) == 0:
        return 'Tie!'

    return None

def get_input():
    while True:
        move = input('Enter your move(example:y x):')
        move = move.strip().split(' ')
        empty_cells = find_empty(board)
        try:
            if len(move) != 2:
                raise Exception('Input must be a coordinate')
            if not (-1 < int(move[0]) < 3 and -1 < int(move[1]) < 3):
                raise Exception('Out of bounds')
            move = [int(move[0]), int(move[1])]
            if move not in empty_cells:
                raise Exception('Occupied cell')
            return move
        except Exception as e:
            print_board(board)
            print(f'Error! {e}. Try again.')


def choose_side():
    while True:
        side = input('Enter your side(X or O):')
        side = side.strip()
        try:
            if side not in ['X', 'O', 'x', 'o']:
                raise Exception('Choose a side')
            return side.upper()
        except Exception as e:
            print(f'Error! {e}. Try again.')


if __name__ == '__main__':

    player = choose_side()
    cpu = 'O' if player == 'X' else 'X'

    if cpu == 'X':
        cpu_move = get_best_move(board)
        board[int(cpu_move[0])][int(cpu_move[1])] = cpu

    while True:
        print_board(board)

        valid_move = get_input()
        board[valid_move[0]][valid_move[1]] = player

        print_board(board)

        winner = win_game(board)
        if winner is not None:
            print(f'The winner is {winner}')
            break

        sleep(1)

        cpu_move = get_best_move(board)
        board[int(cpu_move[0])][int(cpu_move[1])] = cpu

        winner = win_game(board)
        if winner is not None:
            print_board(board)
            print(f'The winner is {winner}')
            break


