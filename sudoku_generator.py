# Angela Carten, William O'Flaherty
# GitHub Link:

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = ['-' * row_length for _ in range(row_length)]
        self.fill_values()
        self.solution = [row[:] for row in self.board]
        self.remove_cells()

    def get_board(self):
        return [row[:] for row in self.board]

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) for num in row))

    def valid_in_row(self, row, num):
        return num in self.board[row]

    def valid_in_col(self, col, num):
        return any(self.board[r][col] == num for r in range(self.row_length))

    def valid_in_box(self, row_start, col_start, num):
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if self.board[r][c] == num:
                    return True
        return False

    def is_valid(self, row, col, num):
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row_start, col_start, num))

    def fill_box(self, row_start, col_start):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        idx = 0
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                self.board[r][c] = numbers[idx]
                idx += 1

    def fill_diagonal(self):
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    def fill_remaining(self):
        for row in range(self.row_length):
            for col in range(self.row_length):
                if self.board[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.fill_remaining():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining()

    def remove_cells(self):
        cells_to_remove = self.removed_cells
        removed_positions = set()
        while cells_to_remove > 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if (row, col) not in removed_positions and self.board[row][col] != 0:
                self.board[row][col] = 0
                removed_positions.add((row, col))
                cells_to_remove -= 1

def generate_sudoku(size, removed):
    generator = SudokuGenerator(size, removed)
    return generator.get_board()