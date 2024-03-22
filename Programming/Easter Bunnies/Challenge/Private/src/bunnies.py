#!/usr/bin/env python
from board import Board


def print_welcome_message(size):
    print(
        "---------------------------------------------------------------------------------------------------------------")
    print("Welcome to an Easter eggs hostage situation!")
    print(
        f"There are {size} boxes & {size} easter bunnies. Each box contains one easter egg numbered from 1-{size}.")
    print(
        f"Every easter bunny may look in less than half of the boxes (less than {size // 2} boxes), this depends on my mood ;).\nGiving each bunny less than 50% to find their egg!")
    print("Unfortunately for you, bunnies can't talk. Meaning they can't tell the other bunnies where their eggs are.")
    print(f"If every easter bunny finds his own easter egg, you win!\nGood luck!")
    print("")
    print("""     .-.            .-.
    /   \          /   \\
   |   _ \        / _   |
   ;  | \ \      / / |  ;
    \  \ \ \_.._/ / /  /
     '. '.;'    ';,' .'
       './ _    _ \.'
       .'  a __ a  '.
  '--./ _,   \/   ,_ \.--'
 ----|   \   /\   /   |----
  .--'\   '-'  '-'    /'--.
      _>.__  -- _.-  `;
    .' _     __/     _/
   /    '.,:".-\    /:,
   |      \.'   `""`'.\\\\
    '-,.__/  _   .-.  ;|_
    /` `|| _/ `\/_  \_|| `\\
   |    ||/ \-./` \ / ||   |
    \   ||__/__|___|__||  /
     \_ |_Happy Easter_| /
    .'  \ =  _= _ = _= /`\\
   /     `-;----=--;--'   \\
   \    _.-'        '.    /
    `""`              `""`""")
    print(
        "---------------------------------------------------------------------------------------------------------------\n")


def find_egg(bunny_number, playing_board: Board):
    print("--------------------------------------")
    print(f"It's bunny {bunny_number} it's turn:")
    attempts_left = playing_board.max_chain
    while attempts_left:
        try:
            print(f"\nYou have {attempts_left} attempts left!")
            box_id = int(input(f"What box would bunny {bunny_number} like to open?\n>>> "))
        except ValueError:
            box_id = -1
        box_contents = playing_board.get_box_contents(box_id)
        if not box_contents:
            print(f"Box {box_id} does not exist!")
        else:
            print(f"Box {box_id} contains {box_contents}")
            if box_contents == bunny_number:
                print(f"Congrats, bunny {bunny_number} found it's egg!\n")
                return True
            else:
                print("That's not quite right...")
        attempts_left -= 1
    return False


def success():
    with open("flag.txt", 'r') as f:
        print(f.readlines()[0])


def play(size):
    print_welcome_message(size)
    playing_board = Board(size)

    cut_off = size // 10

    for bunny in range(1, size + 1):
        if bunny == cut_off:
            print("Hmmm, I think the PrIsOnErS, I mean bunnies, are talking... I definitely should keep them in Chains!")
            print("I'll have to shuffle ALL the eggs after each bunny #TED is Xtreme\n")
        if bunny >= cut_off:
            playing_board.shuffle_eggs()
        if not find_egg(bunny, playing_board):
            print(f"Bunny {bunny} screwed it up! Try again later!")
            return False

    print("\n\nI didn't think you would make it...\nI guess you expect this from me?\n")
    success()


if __name__ == '__main__':
    play(1000)
