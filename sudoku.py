import pygame
from sudoku_generator import generate_sudoku

#Kathryn Allred

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected = None


        if difficulty == "easy":
            removed = 30
        elif difficulty == "medium":
            removed = 40
        else:
            removed = 50

        self.board = generate_sudoku(9, removed)
        self.original = [row[:] for row in self.board]

    def draw(self):
        cell_size = self.width // 9


        for i in range(10):
            if i % 3 == 0:
                line_width = 4
            else:
                line_width = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (self.width, i * cell_size), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, self.height), line_width)


        font = pygame.font.Font(None, 40)
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                if value != 0:
                    text = font.render(str(value), True, (0, 0, 0))
                    self.screen.blit(text, (col * cell_size + 20, row * cell_size + 15))


        if self.selected:
            row, col = self.selected
            pygame.draw.rect(self.screen, (255, 0, 0), (col * cell_size, row * cell_size, cell_size, cell_size), 3)

    def select(self, row, col):
        self.selected = (row, col)

    def click(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            cell_size = self.width // 9
            return (y // cell_size, x // cell_size)
        return None

    def sketch(self, value):
        if self.selected:
            row, col = self.selected
            if self.original[row][col] == 0:
                self.board[row][col] = value

    def place_number(self, value):
        if self.selected:
            row, col = self.selected
            if self.original[row][col] == 0:
                self.board[row][col] = value

    def clear(self):
        if self.selected:
            row, col = self.selected
            if self.original[row][col] == 0:
                self.board[row][col] = 0

    def reset_to_original(self):
        self.board = [row[:] for row in self.original]

    def is_full(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def check_board(self):
        def valid_unit(unit):
            return sorted(unit) == list(range(1, 10))


        for i in range(9):
            row = self.board[i]
            col = [self.board[j][i] for j in range(9)]
            if not valid_unit(row) or not valid_unit(col):
                return False


        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(self.board[box_row + i][box_col + j])
                if not valid_unit(box):
                    return False

        return True




