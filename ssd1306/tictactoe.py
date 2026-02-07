import copy
import random
from time import sleep
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

class TicTacToe:
    

    def __init__(self, diff, player, cpu):
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial)

        self.board = [
        [' ',' ',' '],
        [' ',' ',' '],
        [' ',' ',' ']
        ]
        self.diff = diff
        self.player = player
        self.cpu = cpu

    

    def draw_grid(self, draw):
        draw.line((43, 0, 43, 63), fill="white")
        draw.line((86, 0, 86, 63), fill="white")

        draw.line((0, 21, 127, 21), fill="white")
        draw.line((0, 43, 127, 43), fill="white")
        pass

    def draw_x(self, draw, row, col):
        x1 = 13 + col*42
        y1 = 2 + row*21

        x2 = x1 + 17
        y2 = y1 + 17

        draw.line((x1, y1, x2, y2), fill="white")
        draw.line((x1, y2, x2, y1), fill="white")

    def draw_o(self, draw, row, col):
        x1 = 13 + col*42
        y1 = 2 + row*21

        x2 = x1 + 17
        y2 = y1 + 17

        draw.ellipse((x1, y1, x2, y2), outline="white")

    def print_board(self):
        with canvas(self.device) as draw:
            self.draw_grid(draw)
            for row in range(3):
                for col in range(3):
                    if (self.board[row][col] == "X"):
                        self.draw_x(draw, row, col)
                    elif (self.board[row][col] == "O"):
                        self.draw_o(draw, row, col)


    def find_empty(self, temp_board):
        empty_cells = []
        for x in range(0,3):
            for y in range(0,3):
                if temp_board[y][x] == ' ':
                    empty_cells.append([y,x])
        return empty_cells

    def minimax(self, board ,depth, player_turn, alpha, beta):

        result = self.win_game(board)
        
        

        if result is not None:
            if result == self.player:
                return -10
            elif result == self.cpu:
                return 10
            else:
                return 0
        
        elif (depth == 0):
            return self.evaluate(board)

        else:
            empty_cells = self.find_empty(board)
            if (not empty_cells):
                return 0
            if player_turn == 'MAX':
                best_score = -float('inf')
                for cell in empty_cells:
                    temp_board = copy.deepcopy(board)
                    temp_board[cell[0]][cell[1]] = self.cpu
                    best_score = max(best_score, self.minimax(temp_board, depth - 1, 'MIN', alpha, beta))
                    alpha = max(alpha, best_score)
                    if (alpha >= beta):
                        break
                return best_score
            else:
                best_score = float('inf')
                for cell in empty_cells:
                    temp_board = copy.deepcopy(board)
                    temp_board[cell[0]][cell[1]] = self.player
                    best_score = min(best_score, self.minimax(temp_board, depth - 1, 'MAX', alpha, beta))
                    beta = min(best_score, beta)
                    if (alpha >= beta):
                        break
                return best_score

    def get_best_move(self):
        empty_cells = self.find_empty(self.board)
        temp_board = copy.deepcopy(self.board)
        alpha = -float('inf')
        beta = float('inf')
        best_score = -float('inf')
        best_moves = []
        if len(empty_cells) == 0:
            return None
        else:
            for cell in empty_cells:
                temp_board[cell[0]][cell[1]] = self.cpu
                rec_score = self.minimax(temp_board, self.diff, 'MIN', alpha, beta)
                if best_score < rec_score:
                    best_score = rec_score
                    alpha = best_score
                    best_moves = [cell]
                elif best_score == rec_score:
                    best_moves.append(cell)
                temp_board = copy.deepcopy(self.board)
            return random.choice(best_moves)

    def win_game(self, temp_board):
        empty_cells = self.find_empty(temp_board)
        for x in range(3):
            if temp_board[0][x] == temp_board[1][x] == temp_board[2][x] != ' ':
                return temp_board[0][x]
            elif temp_board[x][0] == temp_board[x][1] == temp_board[x][2] != ' ':
                return temp_board[x][0]

        if temp_board[0][0] == temp_board[1][1] == temp_board[2][2] != ' ':
            return temp_board[0][0]

        elif temp_board[0][2] == temp_board[1][1] == temp_board[2][0] != ' ':
            return temp_board[0][2]

        if len(empty_cells) == 0:
            return 'Tie!'

        return None

    def get_input(self):
        while True:
            move = input('Enter your move(example:y x):')
            move = move.strip().split(' ')
            empty_cells = self.find_empty(self.board)
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
                self.print_board(self.device)
                print(f'Error! {e}. Try again.')

    def evaluate(self, board):
        n = 3
        total_points = 0
        for row in range(n):
            for col in range(n):
                cell_point = 2
                if (row == col):
                    cell_point += 1
                if (row + col == n - 1):
                    cell_point += 1
                if (board[row][col] == 'X'):
                    total_points += cell_point
                elif (board[row][col] == 'O'):
                    total_points -= cell_point
        return total_points


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

def set_difficulty():
    while(True):
        diff = input("""Set difficulty:
            1. Easy
            2. Moderate
            3. Hard\n""")
        try:
            if (len(diff) != 1):
                raise Exception("Difficulty must be a number!")
            diff = int(diff)
            if not (0 < diff < 4):
                raise Exception("Choose a valid difficulty")
            return diff*diff
        except Exception as e:
            print(f'Error {e}. Try Again.')

