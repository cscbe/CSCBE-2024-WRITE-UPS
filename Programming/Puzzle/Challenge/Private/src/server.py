import os
import random
import signal
from typing import List

import numpy as np
from six.moves import input


def generate_reference_array(size: int) -> List[List[int]]:
    # Max size is 9x9 for correct output
    arr = np.arange(1, size**2 + 1)
    arr = arr.reshape(size, size)
    return arr.tolist()


def generate_shuffled_array(size: int) -> List[List[int]]:
    # Max size is 9x9 for correct output
    arr = np.arange(1, size**2 + 1)
    np.random.shuffle(arr)
    arr = arr.reshape(size, size)
    return arr.tolist()


def format_as_table(arr: List[List[int]]) -> str:
    table = ""
    for row in arr:
        table += "+----" * len(row) + "+\n"
        table += "| " + " | ".join(f"{cell:2d}" for cell in row) + " |\n"
    table += "+----" * len(arr[0]) + "+\n"
    return table


def format_moves(moves: str) -> List[str]:
    moves = moves.lower()
    for i in moves:
        if i not in "lrudb":
            raise ValueError(f"Invalid move: {i}, valid moves are l, r, u, d, b.")
    return list(moves)


def check_solution(
    arr: List[List[int]], moves: List[str], cursor_pos: tuple
) -> tuple[bool, List[List[int]]]:
    buffer = 0
    for move in moves:
        if move == "l":
            cursor_pos = (cursor_pos[0], cursor_pos[1] - 1)
        elif move == "r":
            cursor_pos = (cursor_pos[0], cursor_pos[1] + 1)
        elif move == "u":
            cursor_pos = (cursor_pos[0] - 1, cursor_pos[1])
        elif move == "d":
            cursor_pos = (cursor_pos[0] + 1, cursor_pos[1])
        elif move == "b":
            temp_buffer = arr[cursor_pos[0]][cursor_pos[1]]
            arr[cursor_pos[0]][cursor_pos[1]] = buffer
            buffer = temp_buffer

        if (
            cursor_pos[0] < 0
            or cursor_pos[0] >= len(arr)
            or cursor_pos[1] < 0
            or cursor_pos[1] >= len(arr)
        ):
            raise ValueError(f"The cursor is out of bounds.")

    return arr == generate_reference_array(len(arr)), arr


def timeout_handler(signum, frame):
    raise TimeoutError("\nYou're out of time!")


def get_input_with_timeout(prompt, timeout):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    try:
        user_input = input(prompt)
        return user_input
    except TimeoutError as e:
        print(e)
        exit(1)
    finally:
        signal.alarm(0)


def server():
    # TODO: Align text with the lore
    board_size = random.randint(4, 6)
    board = generate_shuffled_array(board_size)

    print(
        f"""
How to play:
1. The cursor starts at the top-left corner
2. Use l, r, u, d to move the cursor left, right, up, or down
3. Use b to place the number at the cursor's position into the buffer, this will also place the number currently in the buffer at the cursor's position
4. You have 10 seconds to send back your solution. Example: 'llduburbdlb'
5. The buffer starts with 0, and must end with 0


Here's an example:
+----+----+----+    +----+----+----+
|  4 |  2 |  9 |    |  1 |  2 |  3 |
+----+----+----+    +----+----+----+
|  3 |  7 |  6 | => |  4 |  5 |  6 |
+----+----+----+    +----+----+----+
|  5 |  8 |  1 |    |  7 |  8 |  9 |
+----+----+----+    +----+----+----+


Aaaand, here is the puzzle:
{format_as_table(board)}
    """
    )

    answer = get_input_with_timeout("Enter your answer: ", 10)

    try:
        is_correct, final_board = check_solution(board, format_moves(answer), (0, 0))
    except ValueError as e:
        print(e)
        exit(1)

    if is_correct:
        print(
            os.getenv(
                "FLAG",
                "There was a problem while retrieving the flag. Please contact an admin.",
            )
        )
    else:
        print("That was not the correct solution.")
        # The following can be uncommented to make things easier
        # print(f"The final board was:\n{format_as_table(final_board)}")
        exit(1)


if __name__ == "__main__":
    server()
