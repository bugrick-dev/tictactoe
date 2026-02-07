from time import sleep
from tictactoe import TicTacToe, choose_side, set_difficulty




if __name__ == '__main__':

    diff = set_difficulty()
    player = choose_side()
    cpu = 'O' if player == 'X' else 'X'

    game = TicTacToe(diff, player, cpu)

    if cpu == 'X':
        cpu_move = game.get_best_move()
        game.board[int(cpu_move[0])][int(cpu_move[1])] = cpu

    while True:
        game.print_board()

        valid_move = game.get_input()
        game.board[valid_move[0]][valid_move[1]] = player

        game.print_board()

        winner = game.win_game(game.board)
        if winner is not None:
            print(f'The winner is {winner}')
            break

        sleep(1)

        cpu_move = game.get_best_move()
        game.board[int(cpu_move[0])][int(cpu_move[1])] = cpu

        winner = game.win_game(game.board)
        if winner is not None:
            game.print_board()
            print(f'The winner is {winner}')
            break