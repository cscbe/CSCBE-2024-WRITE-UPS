import socket
import threading
import random
import os


def start_guessing_game(client_socket, port, flag):
    try:
        max_attempts = len(flag)

        game_message = (
            f"Welcome to the Guessing Game!\nGuess a number between 1 and 100: "
        )
        client_socket.send(game_message.encode())

        number = random.randint(1, 100)
        attempts = -1

        while attempts < max_attempts:
            guess = client_socket.recv(1024).decode().strip()

            if not guess:
                break

            try:
                guess = int(guess)
                if guess == number:
                    correct_message = "Congratulations! You guessed the correct number. Here's part of the flag: CSC{"
                    client_socket.send(correct_message.encode())
                    break
                else:
                    wrong_message = "Wrong guess! Try again: "
                    client_socket.send(wrong_message.encode())
                    attempts += 1

                    # Send one letter of the flag via Out-of-Band data for each incorrect guess
                    if attempts < max_attempts:
                        client_socket.send(flag[attempts].encode(), socket.MSG_OOB)

            except ValueError:
                invalid_message = "Invalid input. Please enter a number: "
                client_socket.send(invalid_message.encode())

        if attempts == max_attempts:
            no_attempts_message = "You've run out of attempts. Better luck next time!"
            client_socket.send(no_attempts_message.encode())

    except Exception as e:
        print(f"Error in guessing game: {e}")
    finally:
        client_socket.close()


def start_netcat_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)

    print(f"Netcat server listening on 0.0.0.0:{port}")

    flag = os.getenv("FLAG", "CSC{ISSUE WITH THE CHALLENGE CALL AN ADMIN!}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            client_thread = threading.Thread(
                target=start_guessing_game, args=(client_socket, port, flag)
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("Server interrupted. Closing.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    netcat_port = 1339
    start_netcat_server(netcat_port)
