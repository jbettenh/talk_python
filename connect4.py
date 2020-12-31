import os
# import sys
import json
from datetime import datetime
from colorama import Fore
import logbook

logbook.set_datetime_format("local")
log_handler = logbook.FileHandler("connect4_application.log", mode='a', encoding=None, level=0, format_string="%Y-%m-%d",
                                  delay=False, filter=None, bubble=False)


def main():
    log_handler.write("App starting up...\n")

    show_leaders()
    board = [
       [None, None, None, None, None, None, None],
       [None, None, None, None, None, None, None],
       [None, None, None, None, None, None, None],
       [None, None, None, None, None, None, None],
       [None, None, None, None, None, None, None],
       [None, None, None, None, None, None, None]
    ]
    active_player_index = 0
    players = get_players()
    symbols = ["Red", "Ylw"]

    while not get_winner(board):
        player = players[active_player_index]
        symbol = symbols[active_player_index]

        show_turn(player)
        # Show the board (6 x 7)
        show_board(board)

        if not get_column(board, symbol):
            print("Please choose a valid column!")
            continue

        active_player_index = (active_player_index + 1) % len(players)

    winner = players[(active_player_index + 1) % len(players)]
    print()
    print()
    print(f" - - - GAME OVER! - - -")
    show_board(board)
    print()
    print(f"{winner} has Won!!")
    print()
    record_highscores(winner)
    log_handler.write(f"{winner} has won! \n")

    log_handler.write("Exiting app \n")


def show_leaders():
    leaders = load_highscores()

    sorted_leaders = list(leaders.items())
    sorted_leaders.sort(key=lambda l: l[1], reverse=True)

    print()
    print("------------------------")
    print("HIGH SCORES:")
    for name, wins in sorted_leaders[0:5]:
        print(f"{name} -- {wins}")
    print("------------------------")
    print()


def show_board(board):

    print("|1|2|3|4|5|6|7|")
    for row in board:
        print("|", end='')
        for cell in row:
            symbol = cell #if cell is not None else "___"
            if symbol == "Red":
                print(Fore.RED + "0" + Fore.WHITE, end='|')
            elif symbol == "Ylw":
                print(Fore.YELLOW + "0" + Fore.WHITE, end='|')
            else:
                print(Fore.WHITE + "_", end='|')
        print()

    print()


def show_turn(player):
    print()
    print(f"It's {player}'s turn!")
    print()


def get_players():
    players = [input("Player 1, what is your name? "), input("Player 2, what is your name? ")]


    log_handler.write(f"{str(players[0])} has logged in \n")
    log_handler.write(f"{str(players[1])} has logged in \n")

    return players


def get_winner(board):
    sequences = get_winning_sequences(board)

    for cells in sequences:
        symbol1 = cells[0]
        if symbol1 and all(symbol1 == cell for cell in cells):
            return True
    return False


def get_column(board, symbol):
    row = len(board) - 1
    col = int(input("Choose which column: "))

    col -= 1

    if col < 0 or col >= len(board[0]):
        return False

    cell = board[row][col]

    while cell is not None and row > 0:
        row -= 1
        cell = board[row][col]

    if cell is not None and row == 0:
        return False

    board[row][col] = symbol

    return True


def get_winning_sequences(board):
    sequences = []
    # Show the board (Row 6 x Col 7)
    # Win by rows
    # board[0][0-7]
    for row_idx1 in range(0, 6):
        row1 = [
                board[row_idx1][0],
                board[row_idx1][1],
                board[row_idx1][2],
                board[row_idx1][3]
            ]
        sequences.append(row1)

    for row_idx2 in range(0, 6):
        row2 = [
            board[row_idx2][1],
            board[row_idx2][2],
            board[row_idx2][3],
            board[row_idx2][4]
        ]
        sequences.append(row2)

    for row_idx3 in range(0, 6):
        row3 = [
            board[row_idx3][2],
            board[row_idx3][3],
            board[row_idx3][4],
            board[row_idx3][5]
        ]
        sequences.append(row3)

    for row_idx4 in range(0, 6):
        row4 = [
            board[row_idx4][3],
            board[row_idx4][4],
            board[row_idx4][5],
            board[row_idx4][6]
        ]
        sequences.append(row4)

    # Win by columns
    for col_idx1 in range(0, 6):
        col = [
            board[2][col_idx1],
            board[3][col_idx1],
            board[4][col_idx1],
            board[5][col_idx1],
        ]
        sequences.append(col)

    for col_idx2 in range(0, 6):
        col2 = [
            board[1][col_idx2],
            board[2][col_idx2],
            board[3][col_idx2],
            board[4][col_idx2],

        ]
        sequences.append(col2)

    for col_idx3 in range(0, 6):
        col3 = [
            board[0][col_idx3],
            board[1][col_idx3],
            board[2][col_idx3],
            board[3][col_idx3],
        ]
        sequences.append(col3)

    # Win by diagonals
    diag1 = [board[0][0], board[1][1], board[2][2], board[3][3]]
    sequences.append(diag1)
    diag2 = [board[0][1], board[1][2], board[2][3], board[3][4]]
    sequences.append(diag2)
    diag3 = [board[0][2], board[1][3], board[2][4], board[3][5]]
    sequences.append(diag3)

    diag4 = [board[1][0], board[2][1], board[3][2], board[4][3]]
    sequences.append(diag4)
    diag5 = [board[1][1], board[2][2], board[3][3], board[4][4]]
    sequences.append(diag5)
    diag6 = [board[1][2], board[2][3], board[3][4], board[4][5]]
    sequences.append(diag6)
    diag7 = [board[1][3], board[2][4], board[3][5], board[3][6]]
    sequences.append(diag7)

    diag8 = [board[2][0], board[3][1], board[4][2], board[5][3]]
    sequences.append(diag8)
    diag9 = [board[2][1], board[3][2], board[4][3], board[5][4]]
    sequences.append(diag9)
    diag10 = [board[2][2], board[3][3], board[4][4], board[5][5]]
    sequences.append(diag10)
    diag11 = [board[2][3], board[3][4], board[4][5], board[5][6]]
    sequences.append(diag11)

    diag12 = [board[0][4], board[1][3], board[2][2], board[3][1]]
    sequences.append(diag12)
    diag13 = [board[0][5], board[1][4], board[2][3], board[3][2]]
    sequences.append(diag13)
    diag14 = [board[0][6], board[1][5], board[2][4], board[3][3]]
    sequences.append(diag14)

    diag15 = [board[1][3], board[2][2], board[3][1], board[4][0]]
    sequences.append(diag15)
    diag16 = [board[1][4], board[2][3], board[3][2], board[4][1]]
    sequences.append(diag16)
    diag17 = [board[1][5], board[2][4], board[3][3], board[4][2]]
    sequences.append(diag17)
    diag18 = [board[1][6], board[2][5], board[3][4], board[4][3]]
    sequences.append(diag18)

    diag19 = [board[2][3], board[3][2], board[4][1], board[5][0]]
    sequences.append(diag19)
    diag20 = [board[2][4], board[3][3], board[4][2], board[5][1]]
    sequences.append(diag20)
    diag21 = [board[2][5], board[3][4], board[4][3], board[5][2]]
    sequences.append(diag21)
    diag22 = [board[2][6], board[3][5], board[4][4], board[5][3]]
    sequences.append(diag22)

    return sequences


""" External File Handling """


def load_highscores():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'highscores.json')

    # Check if file exists
    if not os.path.exists(filename):
        log_handler.write(f"{filename} was not found \n")
        return {}

    with open(filename, 'r', encoding='utf-8') as fin:
        log_handler.write(f"{filename} was found and loaded \n")
        return json.load(fin)


def record_highscores(winner_name):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'highscores.json')
    leaders = load_highscores()

    if winner_name in leaders:
        leaders[winner_name] += 1
    else:
        leaders[winner_name] = 1

    with open(filename, 'w', encoding='utf-8') as fout:
        json.dump(leaders, fout)
        log_handler.write(f"{leaders} were added to {filename} \n")


if __name__ == '__main__':
    with log_handler.applicationbound():
        main()
