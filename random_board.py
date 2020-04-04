from solver import *
from random import shuffle, randint
from copy import deepcopy


empty_board = [[0 for i in range(9)] for j in range(9)]
numbers = [i for i in range(1, 10)]


def check_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return False
    return True


def fill_board(board):
    while True:
        row, col = empty_space(board)
        if board[row][col] == 0:
            shuffle(numbers)
            for value in numbers:
                if valid(board, value, (row, col)):
                    board[row][col] = value
                    if check_board(board):
                        return True
                    else:
                        if fill_board(board):
                            return True
            break

    board[row][col] = 0


fill_board(empty_board)

attempts = 20
while attempts:
    row = randint(0, 8)
    col = randint(0, 8)
    while empty_board[row][col] == 0:
        row = randint(0, 8)
        col = randint(0, 8)

    backup = empty_board[row][col]
    empty_board[row][col] = 0

    copyBoard = deepcopy(empty_board)
    if solve(copyBoard):
        attempts -= 1
    else:
        empty_board[row][col] = 0
        attempts -= 1


print_board(empty_board)
