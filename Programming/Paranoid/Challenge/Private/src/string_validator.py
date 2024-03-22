import logging
import time


class StringValidator:
    CHAR_CHECK_DURATION_SECONDS = 0.25

    def __init__(self, valid_password: str):
        self.VALID_PASSWORD = valid_password

    @staticmethod
    def char_cmp(char1: str, char2: str) -> int:
        if ord(char1) == ord(char2):
            return 0
        return -1 if ord(char1) < ord(char2) else 1

    def check_string(self, guess: str) -> int:
        # Edge case (just in case)
        if guess is None:
            return 1

        # Remove special characters
        guess = guess.encode(encoding='ascii', errors='ignore').decode(encoding='ascii', errors='ignore')
        logging.info(f"Checking '{self.VALID_PASSWORD}' (real) against '{guess}' (guess)")
        # Guess is correct
        if guess == self.VALID_PASSWORD:
            time.sleep(self.CHAR_CHECK_DURATION_SECONDS * (len(guess) + 1))
            return 0

        min_length = min(len(guess), len(self.VALID_PASSWORD))
        guess_clipped = guess[:min_length]
        password_clipped = self.VALID_PASSWORD[:min_length]

        # One is the prefix of the other
        # --> Password validatio fails at the end of the prefix, since the other string is longer
        if guess_clipped == password_clipped:
            time.sleep(self.CHAR_CHECK_DURATION_SECONDS * (min_length + 1))
            # Password is substring of guess --> strcmp('\0', guess[i])
            if len(guess) > len(self.VALID_PASSWORD):
                return -1
            # Guess is substring of password --> strcmp(password[i], '\0')
            else:
                return 1

        # The clipped strings are not equal
        # --> Find the first mistake
        i = 0
        while i < min_length and password_clipped[i] == guess_clipped[i]:
            i += 1
        time.sleep(self.CHAR_CHECK_DURATION_SECONDS * (i + 1))
        return self.char_cmp(password_clipped[i], guess_clipped[i])
