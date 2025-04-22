# Angela Carten,
# GitHub Link:

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[-] * row_length for _ in range(row_length)]
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