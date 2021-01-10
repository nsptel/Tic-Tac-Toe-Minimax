import sys
from copy import deepcopy
import math


def get_possible_pos(state, player):
    pos_moves = []
    temp = deepcopy(state)
    for i, s in enumerate(state):
        if s == 0:
            temp[i] = player
            pos_moves.append((i, temp))
            temp = deepcopy(state)
    return pos_moves


def minimax(state, depth, maximizing_player):
    if Board.winner(state) != 0:
        return {'position': None, 'score': depth * Board.winner(state)}

    if depth == 0:
        return {'position': None, 'score': Board.winner(state)}

    if maximizing_player:
        max_eval = -math.inf
        position = None
        for s in get_possible_pos(state, 1):
            result = minimax(s[1], depth-1, False)
            if result['score'] > max_eval:
                max_eval = result['score']
                position = s[0]
        return {'position': position, 'score': max_eval}
    else:
        min_eval = math.inf
        position = None
        for s in get_possible_pos(state, -1):
            result = minimax(s[1], depth-1, True)
            if result['score'] < min_eval:
                min_eval = result['score']
                position = s[0]
        return {'position': position, 'score': min_eval}


class Board:
    # initializing all the variables
    def __init__(self):
        # creating the board
        self.available_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.user_board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # on the numerical board, X will be 1 and O will be -1
        self.numerical_board = [0 for _ in range(9)]
        self.current_player = 'O'
        self.display_board()

    def display_board(self):
        print("========================================================================")
        print("Current game board (User: 'O', Computer: 'X')")
        print('+-----------+')
        for i in range(1, 10):
            if i % 3 != 0:
                print(f'| {self.user_board[i-1]} ', end='')
            else:
                print(f'| {self.user_board[i-1]} |')
        print('+-----------+')

    @staticmethod
    def winner(m):
        # rows
        count = 0
        for i in range(3):
            s = m[count] + m[count + 1] + m[count + 2]
            if s == 3:
                return 1
            elif s == -3:
                return -1
            count = count + 3
        # columns
        count = 0
        for i in range(3):
            s = m[count] + m[count + 3] + m[count + 6]
            if s == 3:
                return 1
            elif s == -3:
                return -1
            count = count + 1
        # diagonals
        if m[0] + m[4] + m[8] == 3 or m[2] + m[4] + m[6] == 3:
            return 1
        elif m[0] + m[4] + m[8] == -3 or m[2] + m[4] + m[6] == -3:
            return -1
        return 0

    def make_move(self):
        move = -1
        if len(self.available_moves) != 0:
            if self.current_player == 'X':
                # choosing best move
                if len(self.available_moves) == 1:
                    move = self.available_moves[0]
                else:
                    move = minimax(deepcopy(self.numerical_board), len(self.available_moves), True)['position']
                self.available_moves.remove(move)
                self.user_board[move] = 'X'
                self.numerical_board[move] = 1
                self.display_board()
                print(self.numerical_board)
                if Board.winner(self.numerical_board) == 1:
                    print("Computer won the game! Better luck next time.")
                    sys.exit()
                self.current_player = 'O'
            else:
                # get input from the user
                while True:
                    try:
                        move = int(input(f"Your turn. Enter your next move...")) - 1
                        if move not in self.available_moves:
                            raise Exception
                        else:
                            print(move)
                            print(self.available_moves)
                            self.available_moves.remove(move)
                    except:
                        print("Please enter a valid input. Try again.")
                    else:
                        break
                self.user_board[move] = 'O'
                self.numerical_board[move] = -1
                self.display_board()
                if Board.winner(self.numerical_board) == -1:
                    print("You won the game! Congratulations!")
                    sys.exit()
                self.current_player = 'X'


if __name__ == "__main__":
    board = Board()
    while len(board.available_moves) != 0:
        board.make_move()
    else:
        print("The match was a draw!")
