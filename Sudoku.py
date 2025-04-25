import pygame
import sys
import random

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.N = row_length
        self.removed = removed_cells
        self.board = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.fill_values()
        self.solution = [row[:] for row in self.board]
        self.remove_cells()

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return all(self.board[r][col] != num for r in range(self.N))

    def valid_in_box(self, row_start, col_start, num):
        for r in range(3):
            for c in range(3):
                if self.board[row_start + r][col_start + c] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row - row % 3, col - col % 3, num))

    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.N + 1))
        random.shuffle(nums)
        idx = 0
        for r in range(3):
            for c in range(3):
                self.board[row_start + r][col_start + c] = nums[idx]
                idx += 1

    def fill_diagonal(self):
        for i in range(0, self.N, 3):
            self.fill_box(i, i)

    def fill_remaining(self, i=0, j=3):
        if j >= self.N and i < self.N - 1:
            i += 1
            j = 0
        if i >= self.N and j >= self.N:
            return True
        # skip diagonal boxes
        if i < 3:
            if j < 3:
                j = 3
        elif i < self.N - 3:
            if j == int(i / 3) * 3:
                j += 3
        else:
            if j == self.N - 3:
                i += 1
                j = 0
                if i >= self.N:
                    return True
        for num in range(1, self.N + 1):
            if self.is_valid(i, j, num):
                self.board[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    def remove_cells(self):
        count = self.removed
        while count > 0:
            cell_id = random.randrange(0, self.N * self.N)
            row = cell_id // self.N
            col = cell_id % self.N
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1


def generate_sudoku(size, removed):
    gen = SudokuGenerator(size, removed)
    return gen.get_board(), gen.solution

class Cell:
    def __init__(self, value, row, col, width, height, screen):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.temp = value

    def draw(self):
        font = pygame.font.SysFont('comicsans', 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        # Draw number
        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        elif self.temp != 0:
            text = font.render(str(self.temp), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))
        # Draw selection
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, gap, gap), 3)


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.selected = None
        removed = {'easy': 30, 'medium': 40, 'hard': 50}[difficulty]
        board_vals, solution = generate_sudoku(9, removed)
        self.cells = [[Cell(board_vals[r][c], r, c, width, height, screen) for c in range(9)] for r in range(9)]
        self.model = board_vals
        self.solution = solution
        self.difficulty = difficulty

    def draw(self):
        gap = self.width / 9
        for i in range(10):
            thick = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.screen, (0,0,0), (i*gap, 0), (i*gap, self.height), thick)
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected:
            r, c = self.selected
            self.cells[r][c].selected = False
        self.cells[row][col].selected = True
        self.selected = (row, col)

    def click(self, x, y):
        gap = self.width / 9
        if x < self.width and y < self.height:
            return (int(y//gap), int(x//gap))
        return None

    def clear(self):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].temp = 0

    def sketch(self, value):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_cell_value(value)
            self.model[row][col] = value
            return True
        return False

    def reset_to_original(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].value = self.solution[r][c] if self.solution[r][c] != 0 else 0
                self.cells[r][c].temp = 0
                self.model[r][c] = self.cells[r][c].value

    def is_full(self):
        return all(self.model[r][c] != 0 for r in range(9) for c in range(9))

    def update_board(self):
        self.model = [[self.cells[r][c].value for c in range(9)] for r in range(9)]

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.model[r][c] == 0:
                    return (r, c)
        return None

    def check_board(self):
        for r in range(9):
            for c in range(9):
                if self.model[r][c] != self.solution[r][c]:
                    return False
        return True

def main():
    pygame.init()
    width, height = 540, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sudoku")
    font = pygame.font.SysFont('comicsans', 40)

    def draw_start():
        screen.fill((255,255,255))
        title = font.render('Select Difficulty', True, (0,0,0))
        screen.blit(title, (width/2 - title.get_width()/2, 100))
        btns = [('Easy', (width/2-100,200)), ('Medium', (width/2-100,300)), ('Hard', (width/2-100,400))]
        for text, pos in btns:
            rect = pygame.Rect(pos[0], pos[1], 200, 50)
            pygame.draw.rect(screen, (200,200,200), rect)
            label = font.render(text, True, (0,0,0))
            screen.blit(label, (pos[0]+50, pos[1]+5))
        return btns

    def draw_end(win):
        screen.fill((255,255,255))
        msg = 'You Win!' if win else 'Game Over'
        label = font.render(msg, True, (0,0,0))
        screen.blit(label, (width/2 - label.get_width()/2, height/2 - label.get_height()/2))
        pygame.display.update()
        pygame.time.delay(2000)

    running = True
    state = 'start'
    board = None
    btns = []

    while running:
        if state == 'start':
            btns = draw_start()
        elif state == 'playing':
            screen.fill((255,255,255))
            board.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == 'start' and event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                for text,pos in btns:
                    rect = pygame.Rect(pos[0], pos[1], 200, 50)
                    if rect.collidepoint(x,y):
                        board = Board(540,540,screen,text.lower())
                        state = 'playing'
            if state == 'playing':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(*pos)
                    if clicked:
                        board.select(*clicked)
                if event.type == pygame.KEYDOWN:
                    if board.selected:
                        if event.key == pygame.K_1:
                            board.sketch(1)
                        if event.key == pygame.K_2:
                            board.sketch(2)
                        if event.key == pygame.K_3:
                            board.sketch(3)
                        if event.key == pygame.K_4:
                            board.sketch(4)
                        if event.key == pygame.K_5:
                            board.sketch(5)
                        if event.key == pygame.K_6:
                            board.sketch(6)
                        if event.key == pygame.K_7:
                            board.sketch(7)
                        if event.key == pygame.K_8:
                            board.sketch(8)
                        if event.key == pygame.K_9:
                            board.sketch(9)
                        if event.key == pygame.K_RETURN:
                            row,col = board.selected
                            if board.place_number(board.cells[row][col].temp):
                                if board.is_full():
                                    board.update_board()
                                    win = board.check_board()
                                    draw_end(win)
                                    state = 'start'
                            else:
                                pass
                        if event.key == pygame.K_BACKSPACE:
                            board.clear()

        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
