import threading
import socket
import random
import time
import os

# Flags
fake_flag = "have_you_ever_had_a_dream_neo_that_you_were_so_sure_was_real?_hjldsn6349d"
real_flag = os.getenv("FLAG", "CSC{ISSUE WITH THE CHALLENGE CALL AN ADMIN!}")
real_flag = real_flag[4:-1]

# Refresh rate
refresh_time = 0.001

# ANSI escape codes
CLEAR_SCREEN = "\033[2J"
RESET_CURSOR = "\033[H"
GREEN_TEXT = "\033[92m"
RED_TEXT = "\033[91m"
RESET_COLOR = "\033[0m"


def color_text(char, color):
    return f"{color}{char}{RESET_COLOR}"


def modify_random_character(word):
    index_to_modify = random.randint(4, len(word) + 3)
    new_character = random.choice(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    )
    return index_to_modify, new_character


def handle_client(client_socket, address):
    print("Connection established from:", address)

    # initialize screen
    client_socket.send(CLEAR_SCREEN.encode())
    client_socket.send(RESET_CURSOR.encode())

    # print fake flag
    client_socket.send(color_text("CSC{", GREEN_TEXT).encode())
    client_socket.send(color_text(fake_flag, RED_TEXT).encode())
    client_socket.send(color_text("}", GREEN_TEXT).encode())
    time.sleep(3)  # give time to read the fake flag

    # cycle characters
    try:
        for i in range(2000):
            index, char = modify_random_character(real_flag)
            client_socket.send(
                f"\033[0;{index+1}H".encode()
            )  # move cursor to specific character
            client_socket.send(
                color_text(real_flag[index - 4], GREEN_TEXT).encode()
            )  # replace with correct character
            time.sleep(refresh_time)
            client_socket.send(f"\033[0;{index+1}H".encode())
            client_socket.send(
                color_text(char, RED_TEXT).encode()
            )  # replace with random character
            time.sleep(refresh_time)
    except:
        pass
    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 1338))
server_socket.listen(10)

while True:
    client_socket, address = server_socket.accept()
    client_handler = threading.Thread(
        target=handle_client, args=(client_socket, address)
    )
    client_handler.start()
