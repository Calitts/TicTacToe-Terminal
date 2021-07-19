import random
import time

# GLOBAL VARIABLES:
WINNER = "You won!"
DEFALT_WIN = True
BOARD_SIZE = 5
PLAY_AGAIN = True
ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# TODO1: CANCEL MODE IN GAME
# TODO2: WAY TO SELECT MORE THAN ABC PLACES


def getnumbers(i):  # TRANSFORM THE LETTERS TO REFERENCE THE COLLUMS
    table = []
    for j in range(1, i + 1):
        table.append(f"{j}")
    return " ".join(table)


def show(items):  # SHOW THE 2D LIST IN THE TERMINAL
    f = len(items)
    barrier = "---" + "-" * (f * 2) + "--"

    print(f"""\n    {getnumbers(f)} \n{barrier}""")
    for e, item in enumerate(items):
        z = []
        for i in item:
            if i == 1:
                z.append("X")
            elif i == 0:
                z.append("O")
            elif i is None:
                z.append("-")
            elif i == 2:
                z.append("⊘")
            elif i == 3:
                z.append("⨂")

        print(f"{ALFABETO[e]} |", " ".join(z))


def gettable(alfa):  # NOT NESCESSARY - PUT NUMBER IN A DICT TO LETTER
    letters = []
    for letter in alfa:
        letters.append(letter)
    return dict(enumerate(letters))


def getinput(player):  # GETS THE PLAYER INPUT ACORDING TO WHO IS THE TURN
    # AND, TRANFORMS IT IN THE APROPRIEATE FORM TO BE INPUTED IN THE 2D LIST
    try:
        if player == 0:
            j = input("Player O: ")
        elif player == 1:
            j = input("Player X: ")
        place = [letter for letter in j]
        # value_row, value_col = None, None
        collum = place[0].upper()
        row = place[1]
        letter_to_number = {}

        for i, letter in enumerate(ALFABETO):
            letter_to_number[letter] = i
        
        value_col = letter_to_number[collum]
        value_row = int(row)

        return [value_col, value_row]

    except (UnboundLocalError, IndexError):  # MISSPELLS AND INCORRECT TYPES
        print("Put a valid number!")
        value_col, value_row = getinput(player)
        return [value_col, value_row]


# TODO2: In getinput():
# TODO2_resolution: PUT FOR LOOP IN ALFABETO WITH enumerate(),
# TODO2_resolution: INCREASING THE VALUE EACH TIME


def getboard(escala):  # PRODUCES A EMPTY BOARD (2D LIST) ACORDING TO A ESCALE
    game = []
    if escala > 26:
        escala = 26
    for collum in range(escala):
        game.append(list())
        for line in range(escala):
            game[collum].append(None)
    return game


class Turn:  # DEFINE AND GET EACH PLAYER TURN
    def __init__(self, player):
        self.player = player

    def run(self, game):  # GET AND TRANSFORM TABLE ACORDNG TO PLAYER INPUT
        play_col, play_row = getinput(self.player)
        if game[play_col - 1][play_row - 1] is None:
            game[play_col - 1][play_row - 1] = self.player
            return game
        else:  # IF A TAKEN PLACE IS CHOOSEN
            print("This place is unavaiable")
            game = Turn.run(self, game)
            return game

    def won_table(self, board, original, first, second):
        orig1, orig2 = original[0], original[1]
        fst1, fst2 = first[0], first[1]
        sec1, sec2 = second[0], second[1]

        board[orig1][orig2] = self.player + 2
        board[fst1][fst2] = self.player + 2
        board[sec1][sec2] = self.player + 2
        show(board)
        Turn.won(self)

    def won(self):

        if self.player == 1:
            print("Player X won!")

        elif self.player == 0:
            print("Player O won!")

    def rowformation(self, row, i, j, board):
        global win
        if (
            row[i - 1] == self.player
            and row[i + 1] == self.player
            and row[i] == self.player
        ):
            Turn.won_table(self, board, (j, i), (j, i - 1), (j, i + 1))
            win = not again()
            return win
        return False

    def collumformation(self, board, point):
        global win
        for position, item in enumerate(board):
            if (
                board[point - 1][position] == self.player
                and board[point + 1][position] == self.player
                and board[point][position] == self.player
            ):
                Turn.won_table(
                    self,
                    board,
                    (point, position),
                    (point - 1, position),
                    (point + 1, position),
                )
                win = not again()
                return win
        return False

    def xformation(self, board, i, j):
        global win
        if (
            board[j - 1][i - 1] == self.player
            and board[j + 1][i + 1] == self.player
            and board[j][i] == self.player
        ):
            Turn.won_table(self, board, (j, i), (j - 1, i - 1), (j + 1, i + 1))
            win = not again()
            return win

        elif (
            board[j - 1][i + 1] == self.player
            and board[j + 1][i - 1] == self.player
            and board[j][i] == self.player
        ):
            Turn.won_table(self, board, (j, i), (j - 1, i + 1), (j + 1, i - 1))
            win = not again()
            return win

        return False

    def formation(self, board):
        win = False
        for j, row in enumerate(board):
            if not win:
                for i, point in enumerate(row):

                    if point is not None:

                        if not (i <= 0) and not (i >= BOARD_SIZE - 1):
                            win = Turn.rowformation(self, row, i, j, board)
                            break

                        if not (i <= 0) and not (i >= BOARD_SIZE - 1):
                            if not bool(j <= 0) and not bool(j >= (BOARD_SIZE - 1)):
                                win = Turn.xformation(self, board, i, j)
                                break

                        if not (j <= 0) and not (j >= BOARD_SIZE - 1):
                            win = Turn.collumformation(self, board, j)
                            break

        if win:
            return win

        return False


def again():  # CHECK IF WANTS TO PLAY AGAIN
    print("Gamer Over!")
    repeat = input("Play again?(y/n)\n")
    if repeat == "y":
        main()
    else:
        time.sleep(0.5)
        run = False
    return run


def empty(game, run=True):  # CHECK FOR EMPTY ESPACES
    z = 0
    for collum in game:
        for point in collum:
            if point is None:
                z += 1
    if z == 0 and PLAY_AGAIN:  # IF ANY, PREPARES TO END THE GAME
        run = again()
        return run

    return run


def main():  # MAIN CODE, WITH SOME TESTS FOR DEBUGGING
    # print(play1_col-1, play1_row-1)
    # print(game[play1_col-1][play1_row-1])
    # print(game[play2_col-1][play2_row-1])

    first = random.randint(0, 1)

    player1 = Turn(first)
    player2 = Turn(first - 1 if (first == 1) else first + 1 if (first == 0) else None)
    run = True
    win = False
    game = getboard(BOARD_SIZE)  # SETS THE BOARD SIZE AND SHOWS IT
    show(game)

    while not win and run:  # MAIN GAME-LOOP
        game = player1.run(game)  # PLAYER 1 TURN, WITH BOARD SHOW
        show(game)
        win = player1.formation(game)
        run = empty(game)
        if not run or win:
            break
        game = player2.run(game)  # PLAYER 2 TURN, WITH BOARD SHOW
        show(game)
        win = player2.formation(game)
        run = empty(game)
        if not run or win:
            break


if __name__ == "__main__":
    main()
