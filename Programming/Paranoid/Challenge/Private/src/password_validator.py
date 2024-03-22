import os

from string_validator import StringValidator


class PasswordValidator:

    def __init__(self):
        self.VALID_PASSWORD = os.environ['password']

    def check_password(self, guess: str) -> int:
        return StringValidator(self.VALID_PASSWORD).check_string(guess)
