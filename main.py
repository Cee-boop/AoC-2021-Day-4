with open(file='data.txt') as file:
    numbers, board_breakdown = [int(num) for num in file.readline().strip().split(",")], [row.rstrip().lstrip().split(" ") for row in file.read().strip().split("\n") if len(row) > 1]
    boards = []
    for index, row in enumerate(board_breakdown):
        boards.append([])
        for number in row:
            if number:
                boards[index].append(int(number))

#####################################################################
BINGO_NUMBERS = numbers
ROW_LENGTH = 5
COL_LENGTH = 5


class BingoBoard:

    def __init__(self, board_data, board_index_pos):
        self.board = [board_data[row] for row in range(len(board_data))]
        self.board_index_pos = board_index_pos
        self.winning_board = False
        self.is_faster = False
        self.is_slower = False
        self.call_numbers()

    def call_numbers(self):
        global fastest_game, slowest_game
        for i, call_out in enumerate(BINGO_NUMBERS):
            for r, row in enumerate(self.board):
                for c, n in enumerate(row):

                    if self.board[r][c] == call_out:
                        self.board[r][c] = "X"
                        self.check_row(i)
                        self.check_column(i)
                        if self.winning_board:
                            self.winning_board_sum()
                            print(f"board: {self.board}, "
                                  f"board count: {self.board_index_pos}, "
                                  f"fastest game: {fastest_game}, "
                                  f"slowest game: {slowest_game}")
                            return

    def check_row(self, number_index):
        for row in self.board:
            if row.count("X") == 5:
                self.log_results(number_index)
                return

    def check_column(self, number_index):
        for c in range(ROW_LENGTH):
            column = []
            for r in range(COL_LENGTH):
                column.append(self.board[r][c])
                if column.count("X") == 5:
                    self.log_results(number_index)
                    return

    def log_results(self, number_index):
        global fastest_game, slowest_game
        if number_index < fastest_game['call_index']:
            self.is_faster = True
            fastest_game['call_index'] = number_index
            fastest_game['winning_number'] = BINGO_NUMBERS[number_index]
            fastest_game['board_number'] = self.board_index_pos
        if number_index > slowest_game['call_index']:
            self.is_slower = True
            slowest_game['call_index'] = number_index
            slowest_game['winning_number'] = BINGO_NUMBERS[number_index]
            slowest_game['board_number'] = self.board_index_pos
        self.winning_board = True

    def winning_board_sum(self):
        global fastest_game, slowest_game
        board_sum = 0
        for r, row in enumerate(self.board):
            for c, col in enumerate(row):
                if self.board[r][c] != "X":
                    board_sum += self.board[r][c]

        if self.is_faster:
            fastest_game['board_sum'] = board_sum * fastest_game['winning_number']
        if self.is_slower:
            slowest_game['board_sum'] = board_sum * slowest_game['winning_number']


fastest_game = {'board_number': float('inf'), 'call_index': float('inf'), 'winning_number': -1, 'board_sum': -1}
slowest_game = {'board_number': float('-inf'), 'call_index': float('-inf'), 'winning_number': -1, 'board_sum': -1}

i, j = 0, 5  # board parsing window
curr_board_index = 0
while boards:
    BingoBoard(boards[i:j], curr_board_index)
    boards = boards[j:]
    curr_board_index += 1

# part one:
print(fastest_game['board_sum'])
# part two:
print(slowest_game['board_sum'])
