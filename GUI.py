import pygame
from solver import solve, valid
from random_board import remove_nums

pygame.font.init()


class Grid:

    def __init__(self, board, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thickness)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thickness)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, pos):
    win.fill((255, 255, 255))
    # Draw grid, board and buttons
    y_pos = 550 < pos[1] < 590
    # highlight single button
    if 160 > pos[0] > 10 and y_pos:
        pygame.draw.rect(win, (150, 150, 150), (10, 550, 150, 40), 0)
        handle_text(win)
    elif 330 > pos[0] > 180 and y_pos:
        pygame.draw.rect(win, (150, 150, 150), (195, 550, 150, 40), 0)
        handle_text(win)
    elif 500 > pos[0] > 350 and y_pos:
        pygame.draw.rect(win, (150, 150, 150), (380, 550, 150, 40), 0)
        handle_text(win)
    else:
        pygame.draw.rect(win, (200, 200, 200), (10, 550, 150, 40), 0)
        pygame.draw.rect(win, (200, 200, 200), (195, 550, 150, 40), 0)
        pygame.draw.rect(win, (200, 200, 200), (380, 550, 150, 40), 0)
        handle_text(win)
    board.draw(win)


def handle_text(win):
    fnt = pygame.font.SysFont("comicsans", 30)
    text_easy = fnt.render("Easy", True, (0, 0, 0))
    text_medium = fnt.render("Medium", True, (0, 0, 0))
    text_expert = fnt.render("Expert", True, (0, 0, 0))
    rect_easy = text_easy.get_rect(center=(80, 570))
    rect_medium = text_easy.get_rect(center=(255, 570))
    rect_expert = text_easy.get_rect(center=(450, 570))
    win.blit(text_easy, rect_easy)
    win.blit(text_medium, rect_medium)
    win.blit(text_expert, rect_expert)


def button_pressed(pos):
    pass


def main():
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(remove_nums("easy"), 9, 9, 540, 540)
    pygame.draw.rect(window, (200, 200, 200), (10, 550, 150, 40), 0)
    pygame.draw.rect(window, (200, 200, 200), (195, 550, 150, 40), 0)
    pygame.draw.rect(window, (200, 200, 200), (380, 550, 150, 40), 0)
    handle_text(window)
    key = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

            pos = pygame.mouse.get_pos()

        if board.selected and key is not None:
            board.sketch(key)

        redraw_window(window, board, pos)
        pygame.display.update()


main()
pygame.quit()
