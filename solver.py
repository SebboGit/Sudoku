easy_board = [
    [0, 0, 6, 8, 2, 0, 9, 0, 7],
    [0, 0, 4, 3, 0, 0, 0, 0, 0],
    [0, 8, 0, 4, 9, 0, 0, 3, 1],
    [0, 0, 0, 0, 3, 2, 1, 0, 0],
    [5, 1, 0, 9, 0, 0, 3, 0, 0],
    [0, 0, 0, 1, 0, 0, 7, 6, 8],
    [2, 7, 0, 0, 0, 9, 0, 0, 0],
    [6, 3, 0, 0, 1, 4, 0, 0, 2],
    [8, 0, 0, 0, 0, 0, 6, 5, 0]
]


def solve(board):
    if not empty_space(board):
        return True
    else:
        row, col = empty_space(board)

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


def empty_space(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(board, num, position):
    # row
    for i in range(len(board[0])):
        if board[position[0]][i] == num and position[1] != i:
            return False

    # column
    for i in range(len(board)):
        if board[i][position[1]] == num and position[0] != i:
            return False

    # box
    x_val = position[1] // 3
    y_val = position[0] // 3

    for i in range(y_val * 3, y_val * 3 + 3):
        for j in range(x_val * 3, x_val * 3 + 3):
            if board[i][j] == num and (i, j) != position:
                return False

    return True


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - -")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


print_board(easy_board)
solve(easy_board)
print_board(easy_board)