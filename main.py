with open(file='data.txt') as file:
    numbers, board_breakdown = [int(num) for num in file.readline().strip().split(",")], [row.rstrip().lstrip().split(" ") for row in file.read().strip().split("\n") if len(row) > 1]
    data = []
    for index, row in enumerate(board_breakdown):
        data.append([])
        for number in row:
            if number:
                data[index].append(int(number))

#####################################################################
BINGO_NUMBERS = numbers
ROW_LENGTH = 5
COL_LENGTH = 5


class BingoBoard:

    def __init__(self, board_data, board_index):
        self.template = [board_data[row] for row in range(len(board_data))]
        self.board_index = board_index
        self.is_winning_board = False
        self.is_faster = False
        self.is_slower = False

    def look_for(self, n):
        for r, row in enumerate(self.template):
            for c, col in enumerate(row):
                if self.template[r][c] == n:
                    # if number present, mark board
                    self.template[r][c] = "X"

    def check_row(self, number_index):
        for row in self.template:
            if row.count("X") == 5:
                self.log_results(number_index)
                return

    def check_column(self, number_index):
        for c in range(ROW_LENGTH):
            column = []
            for r in range(COL_LENGTH):
                column.append(self.template[r][c])
                if column.count("X") == 5:
                    self.log_results(number_index)
                    return

    def log_results(self, number_index):
        global fastest_game, slowest_game
        if number_index < fastest_game['call_index']:
            self.is_faster = True
            fastest_game['call_index'] = number_index
            fastest_game['winning_number'] = BINGO_NUMBERS[number_index]
            fastest_game['board_number'] = self.board_index
        if number_index > slowest_game['call_index']:
            self.is_slower = True
            slowest_game['call_index'] = number_index
            slowest_game['winning_number'] = BINGO_NUMBERS[number_index]
            slowest_game['board_number'] = self.board_index
        self.is_winning_board = True

    def winning_sum(self):
        global fastest_game, slowest_game
        board_sum = 0
        for r, row in enumerate(self.template):
            for c, col in enumerate(row):
                if self.template[r][c] != "X":
                    board_sum += self.template[r][c]

        if self.is_faster:
            fastest_game['board_sum'] = board_sum * fastest_game['winning_number']
        if self.is_slower:
            slowest_game['board_sum'] = board_sum * slowest_game['winning_number']


# --------------------------------------------------------------------------------------------------------------------
fastest_game = {'board_number': float('inf'), 'call_index': float('inf'), 'winning_number': -1, 'board_sum': -1}
slowest_game = {'board_number': float('-inf'), 'call_index': float('-inf'), 'winning_number': -1, 'board_sum': -1}

i, j = 0, 5  # board parsing window
curr_board_index = 0
bingo_boards = []
while data:
    new_board = BingoBoard(data[i:j], curr_board_index)
    bingo_boards.append(new_board)
    data = data[j:]
    curr_board_index += 1

for curr_board in bingo_boards:
    # start calling numbers...
    for i, number in enumerate(BINGO_NUMBERS):
        curr_board.look_for(number)
        curr_board.check_row(i)
        curr_board.check_column(i)
        if curr_board.is_winning_board:
            curr_board.winning_sum()
            print(f"board: {curr_board.template} board number: {curr_board.board_index}, "
                  f"fastest game: {fastest_game}, slowest game: {slowest_game}")
            break


# part one:
print(fastest_game['board_sum'])
# part two:
print(slowest_game['board_sum'])

