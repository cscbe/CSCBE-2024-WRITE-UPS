import sys

from pwn import remote


def extract_puzzle(input_data: bytes) -> list[list[int]]:
    raw_lines = input_data.decode("utf-8").split("\n")
    puzzle_lines = raw_lines[
        raw_lines.index(
            next(line for line in raw_lines if "Aaaand, here is the puzzle:" in line)
        ) + 1 : -3
    ]
    puzzle = []
    for i, line in enumerate(puzzle_lines):
        if i % 2 == 0:
            continue
        numbers = [int(x) for x in line.split("|")[1:-1]]
        puzzle.append(numbers)
    return puzzle


def generate_reference_board(size: int) -> list[list[int]]:
    arr = list(range(1, size**2 + 1))
    arr = [arr[i : i + size] for i in range(0, len(arr), size)]
    return arr


def find_number_position(buffer_value: int, board: list[list[int]]):
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == buffer_value:
                return i, j


def move_cursor(
    cursor_pos: tuple[int, int], dest_row: int, dest_col: int, solution: list[str]
) -> tuple[int, int]:
    while cursor_pos != (dest_row, dest_col):
        if cursor_pos[0] < dest_row:
            solution.append("d")
            cursor_pos = (cursor_pos[0] + 1, cursor_pos[1])
        elif cursor_pos[0] > dest_row:
            solution.append("u")
            cursor_pos = (cursor_pos[0] - 1, cursor_pos[1])
        elif cursor_pos[1] < dest_col:
            solution.append("r")
            cursor_pos = (cursor_pos[0], cursor_pos[1] + 1)
        elif cursor_pos[1] > dest_col:
            solution.append("l")
            cursor_pos = (cursor_pos[0], cursor_pos[1] - 1)
    return cursor_pos


def generate_solution(puzzle):
    cursor_pos = (0, 0)
    board_size = len(puzzle)
    reference_board = generate_reference_board(board_size)
    buffer_value = 0

    solution = []
    for number in range(1, board_size**2 + 1):
        try:
            src_row, src_col = find_number_position(number, puzzle)
            cursor_pos = move_cursor(cursor_pos, src_row, src_col, solution)

            temp_buffer = int(puzzle[cursor_pos[0]][cursor_pos[1]])
            puzzle[cursor_pos[0]][cursor_pos[1]] = buffer_value
            buffer_value = temp_buffer
            solution.append("b")
        except:
            pass

        dest_row, dest_col = find_number_position(number, reference_board)
        cursor_pos = move_cursor(cursor_pos, dest_row, dest_col, solution)

        temp_buffer = int(puzzle[cursor_pos[0]][cursor_pos[1]])
        puzzle[cursor_pos[0]][cursor_pos[1]] = buffer_value
        buffer_value = temp_buffer
        solution.append("b")

    return "".join(solution)


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])

    r = remote(host, port)
    raw_input = r.recvuntil("Enter your answer:")

    puzzle = extract_puzzle(raw_input)
    solution = generate_solution(puzzle)

    r.sendline(solution.encode())
    print(r.recvall())
