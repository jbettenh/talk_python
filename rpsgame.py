import os
import datetime
import random
import json

rolls = {}


def main():
    log("App starting up...")

    load_rolls()
    show_header()
    show_leaders()

    player1, player2 = get_players()
    log(f"{player1} has logged in.")
    play_game(player1, player2)
    log("Exit app")


def load_rolls():
    global rolls

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'rolls.json')

    with open(filename, 'r', encoding='utf-8') as fin:
        rolls = json.load(fin)

    log(f"Loaded rolls: {list(rolls.keys())} from {os.path.basename(filename)}.")


def load_leaders():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json')

    if not os.path.exists(filename):
        return {}

    with open(filename, 'r', encoding='utf-8') as fin:
        return json.load(fin)


def show_header():
    print("------------------------")
    print("Rock Paper Scissors v2.0")
    print("  File I/O Edition")
    print("------------------------")


def show_leaders():
    leaders = load_leaders()

    sorted_leaders = list(leaders.items())
    sorted_leaders.sort(key=lambda l: l[1], reverse=True)

    print()
    print("Leaderboard:")
    for name, wins in sorted_leaders[0:5]:
        print(f"{wins} -- {name}")
    print()
    print("------------------------")


def get_players():
    p1 = input("Player 1, what is your name? ")
    p2 = "Computer"

    return p1, p2


def play_game(player_1, player_2):
    log(f"New game starting between {player_1} and {player_2}.")
    rounds = 3
    wins_p1 = 0
    wins_p2 = 0

    roll_names = list(rolls.keys())

    while wins_p1 < rounds and wins_p2 < rounds:
        roll1 = get_roll(player_1, roll_names)
        roll2 = random.choice(roll_names)

        if not roll1:
            print("Try again!")
            continue

        print(f"{player_1} rolls {roll1}")
        print(f"{player_2} rolls {roll2}")

        winner = check_for_winning_throw(player_1, player_2, roll1, roll2)

        if winner is None:
            print("This round was a tie!")
        else:
            print(f"{winner} takes the round!")
            if winner == player_1:
                wins_p1 += 1
            elif winner == player_2:
                wins_p2 += 1

        msg = f"Score is {player_1}: {wins_p1} and {player_2}: {wins_p2}."
        print(msg)
        log(msg)
        print()

    if wins_p1 >= rounds:
        overall_winner = player_1
    else:
        overall_winner = player_2

    msg = f"{overall_winner} wins the game!"
    print(msg)
    log(msg)
    record_win(overall_winner)


def check_for_winning_throw(player_1, player_2, roll1, roll2):
    winner = None
    if roll1 == roll2:
        print("The play was tied!")

    outcome = rolls.get(roll1, {})
    if roll2 in outcome.get('defeats'):
        return player_1
    elif roll2 in outcome.get('defeated_by'):
        return player_2

    return winner


def get_roll(player_name, roll_names):
    print("Available rolls:")
    for index, r in enumerate(roll_names, start=1):
        print(f"{index}.{r}")

    text = input(f"{player_name}, what is your roll? ")
    selected_index = int(text) - 1

    if selected_index < 0 or selected_index >= len(rolls):
        print(f"Sorry {player_name}, {text} is out of bounds!")
        return None

    return roll_names[selected_index]


def record_win(winner_name):
    leaders = load_leaders()
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json')

    if winner_name in leaders:
        leaders[winner_name] += 1
    else:
        leaders[winner_name] = 1

    with open(filename, 'w', encoding='utf-8') as fout:
        json.dump(leaders, fout)


def log(msg):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'rps.log')
    time_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(filename, 'a', encoding='utf-8') as fout:
        fout.write(f"[{time_text}] ")
        fout.write(msg)
        fout.write('\n')


if __name__ == '__main__':
    main()
