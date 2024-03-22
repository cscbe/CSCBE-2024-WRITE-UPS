import os
import random
import time
import unittest
import uuid

from flask_server import APP
from otp_manager import OTPManager
from password_validator import PasswordValidator
from string_validator import StringValidator


def _binary_search_timing_attack(check_function, max_length):
    alphabet = [chr(i) for i in range(128)]
    mid = 0
    guess = ""
    current_duration = StringValidator.CHAR_CHECK_DURATION_SECONDS
    result = -1

    while result != 0 and len(guess) < max_length:
        low = 0
        high = len(alphabet) - 1
        while low <= high:
            mid = (high + low) // 2
            char = alphabet[mid]
            start = time.time()
            print(f"checking {guess + char}")
            result = check_function(guess + char)
            duration = time.time() - start

            if duration - (StringValidator.CHAR_CHECK_DURATION_SECONDS / 2) > current_duration:
                current_duration = duration
                guess += char
                break

            # If 'strcmp' return 1, ignore left half
            if result == 1:
                low = mid + 1

            # If 'strcmp' return -1, ignore right half
            elif result == -1:
                high = mid - 1
    if result != 0:
        return "Timeout: guessed password is too long"
    return guess


def _brute_force_timing_attack(check_function, max_length):
    alphabet = [chr(i) for i in range(128)]
    guess = ""
    current_duration = StringValidator.CHAR_CHECK_DURATION_SECONDS
    result = -1
    while result != 0 and len(guess) < max_length:
        for char in alphabet:
            start = time.time()
            result = check_function(guess + char)
            duration = time.time() - start
            if duration - (StringValidator.CHAR_CHECK_DURATION_SECONDS / 2) > current_duration:
                current_duration = duration
                guess += char
                print(guess)
                break
    if result != 0:
        return "Timeout: guessed password is too long"
    return guess


class TestPassword(unittest.TestCase):

    def __init__(self, methodName: str = 'runTest'):
        super().__init__(methodName=methodName)
        self.PV = PasswordValidator()
        self.VALID_PASSWORD = self.PV.VALID_PASSWORD

    # Basic tests
    def test_password_validator_correct(self):
        result = self.PV.check_password(self.VALID_PASSWORD)
        self.assertEqual(result, 0)

    def test_password_validator_wrong_different(self):
        result = self.PV.check_password("random guess")
        self.assertNotEqual(result, 0)

    def test_password_validator_wrong_too_long(self):
        result = self.PV.check_password(self.VALID_PASSWORD + " ")
        self.assertNotEqual(result, 0)

    def test_password_validator_wrong_too_short(self):
        result = self.PV.check_password(self.VALID_PASSWORD[:-2])
        self.assertNotEqual(result, 0)

    def test_password_validator_wrong_lower_case(self):
        result = self.PV.check_password(self.VALID_PASSWORD.lower())
        self.assertNotEqual(result, 0)

    def test_password_validator_wrong_upper_case(self):
        result = self.PV.check_password(self.VALID_PASSWORD.upper())
        self.assertNotEqual(result, 0)

    def test_password_validator_wrong_extra_whitespaces(self):
        # Remove artificial delay for this test
        old_delay = StringValidator.CHAR_CHECK_DURATION_SECONDS
        StringValidator.CHAR_CHECK_DURATION_SECONDS = 0

        for i in range(len(self.VALID_PASSWORD)):
            for j in range(1, 3):
                for whitespace in (' ', '\t', '\n'):
                    password_with_whitespace = f"{self.VALID_PASSWORD[:i]}{whitespace}{self.VALID_PASSWORD[i:]}"
                    result = self.PV.check_password(password_with_whitespace)
                    self.assertNotEqual(result, 0)

        # Re-enable artificial delay for other tests
        StringValidator.CHAR_CHECK_DURATION_SECONDS = old_delay

    def test_password_validator_wrong_empty_string(self):
        result = self.PV.check_password("")
        self.assertNotEqual(result, 0)

    # noinspection PyTypeChecker
    def test_password_validator_wrong_none(self):
        result = self.PV.check_password(None)
        self.assertNotEquals(result, 0)

    def test_password_validator_wrong_unicode(self):
        result = self.PV.check_password("😁😊😂🤣")
        self.assertNotEquals(result, 0)
        result = self.PV.check_password("Ståle")
        self.assertNotEquals(result, 0)

    # Check return value
    def test_password_validator_higher_ascii_value(self):
        # Remove artificial delay for this test
        old_delay = StringValidator.CHAR_CHECK_DURATION_SECONDS
        StringValidator.CHAR_CHECK_DURATION_SECONDS = 0

        for i in range(len(self.VALID_PASSWORD)):
            new_char = chr(random.randrange(ord(self.VALID_PASSWORD[i]) + 1, 128))
            wrong_password_higher = f"{self.VALID_PASSWORD[:i]}{new_char}{self.VALID_PASSWORD[i + 1:]}"
            result = self.PV.check_password(wrong_password_higher)
            self.assertEqual(result, -1)

        # Re-enable artificial delay for other tests
        StringValidator.CHAR_CHECK_DURATION_SECONDS = old_delay

    def test_password_validator_lower_ascii_value(self):
        # Remove artificial delay for this test
        old_delay = StringValidator.CHAR_CHECK_DURATION_SECONDS
        StringValidator.CHAR_CHECK_DURATION_SECONDS = 0

        for i in range(len(self.VALID_PASSWORD)):
            new_char = chr(random.randrange(1, ord(self.VALID_PASSWORD[i]) - 1))
            wrong_password_higher = f"{self.VALID_PASSWORD[:i]}{new_char}{self.VALID_PASSWORD[i + 1:]}"
            result = self.PV.check_password(wrong_password_higher)
            self.assertEqual(result, 1)

        # Re-enable artificial delay for other tests
        StringValidator.CHAR_CHECK_DURATION_SECONDS = old_delay

    def test_check_brute_force_attack_works(self):  # Takes about 10 minutes
        guess = _brute_force_timing_attack(self.PV.check_password, len(self.PV.VALID_PASSWORD))
        self.assertEqual(guess, self.PV.VALID_PASSWORD)

    def test_check_binary_search_timing_attack_works(self):
        guess = _binary_search_timing_attack(self.PV.check_password, len(self.PV.VALID_PASSWORD))
        self.assertEqual(guess, self.PV.VALID_PASSWORD)


class TestPasswordIntegration(unittest.TestCase):

    def test_password_correct(self):
        password = PasswordValidator().VALID_PASSWORD
        response = APP.test_client().post('validate', json={'password': password})
        self.assertEqual(response.status_code, 200)

    def test_password_incorrect(self):
        response = APP.test_client().post('validate', json={'password': 'This is a wrong password'})
        self.assertEqual(response.status_code, 401)

    def test_password_wrong_too_long(self):
        password = PasswordValidator().VALID_PASSWORD
        response = APP.test_client().post('validate', json={'password': password + '1'})
        self.assertEqual(response.status_code, 401)

    def test_password_wrong_too_short(self):
        password = PasswordValidator().VALID_PASSWORD
        response = APP.test_client().post('validate', json={'password': password[:-1]})
        self.assertEqual(response.status_code, 401)

    def test_password_not_supplied(self):
        response = APP.test_client().post('validate', json={})
        self.assertEqual(response.status_code, 400)

    def test_password_empty(self):
        response = APP.test_client().post('validate', json={'password': ''})
        self.assertEqual(response.status_code, 401)

    def test_password_None(self):
        response = APP.test_client().post('validate', json={'password': None})
        self.assertEqual(response.status_code, 401)


class TestOTP(unittest.TestCase):
    def __init__(self, methodName: str = 'runTest'):
        super().__init__(methodName=methodName)
        self.OTPM = OTPManager()

    def test_new_guid_registered_limited_tries_left(self):
        guid = str(uuid.uuid4())
        # GUID does not exist yet
        self.assertFalse(self.OTPM.check_otp_active(guid))
        with self.assertRaises(KeyError):
            self.OTPM.update_otp_counter(guid)

        # Now register the GUID
        self.OTPM.enable_otp(guid)

        # GUID is registered
        self.assertTrue(self.OTPM.check_otp_active(guid))

        for tries_left in range(OTPManager.OTP_MAX_TRIES, 0, -1):
            self.assertEqual(self.OTPM.ACTIVE_OTP_TRIES[guid], tries_left)
            self.OTPM.update_otp_counter(guid)  # Try GUID

        # After OTP_MAX_TRIES tries, the GUID should not be registered anymore
        self.assertFalse(self.OTPM.check_otp_active(guid))
        with self.assertRaises(KeyError):
            self.OTPM.update_otp_counter(guid)

    def test_generate_otps_valid_chars(self):
        for _ in range(100_000):
            otp = self.OTPM.generate_otp()
            self.assertTrue(len(otp) == self.OTPM.OTP_LENGTH)
            for char in otp:
                self.assertTrue(char.isalnum())

    def test_generate_otps_random_unique(self):
        generated_otps = [self.OTPM.generate_otp() for _ in range(1_000)]
        print(f"First 10 generated OTPs: {generated_otps[:10]}")
        # If the list of OTPs is equal in length to the set, all OTPs in the list are unique
        self.assertEqual(len(set(generated_otps)), len(generated_otps))

    # Not too many checks for this, since it uses the same code as the Password validator
    def test_check_otp_correct(self):
        guid = str(uuid.uuid4())
        self.OTPM.enable_otp(guid)
        otp = self.OTPM.ACTIVE_OTP_CODES[guid]
        result = self.OTPM.check_otp(otp, guid)
        self.assertEqual(result, 0)

    def test_check_otp_wrong_too_long(self):
        guid = str(uuid.uuid4())
        self.OTPM.enable_otp(guid)
        otp = self.OTPM.ACTIVE_OTP_CODES[guid] + "EXRTA"
        result = self.OTPM.check_otp(otp, guid)
        self.assertEqual(result, -1)

    def test_check_otp_wrong_too_short(self):
        guid = str(uuid.uuid4())
        self.OTPM.enable_otp(guid)
        otp = self.OTPM.ACTIVE_OTP_CODES[guid][:-1]
        result = self.OTPM.check_otp(otp, guid)
        self.assertEqual(result, 1)

    def test_check_otp_wrong_none(self):
        guid = str(uuid.uuid4())
        self.OTPM.enable_otp(guid)
        otp = None
        result = self.OTPM.check_otp(otp, guid)
        self.assertEqual(result, 1)


class TestOTPIntegration(unittest.TestCase):
    def test_otp_wrong(self):
        backend = APP.test_client()
        password = PasswordValidator().VALID_PASSWORD

        pass_response = backend.post('validate', json={'password': password})
        self.assertEqual(pass_response.status_code, 200)

        guid = eval(pass_response.data)['message'][1:]
        otp_response = backend.post(guid, json={'otp': 'TEST12'})
        self.assertEqual(otp_response.status_code, 401)

    def test_otp_not_supplied(self):
        backend = APP.test_client()
        password = PasswordValidator().VALID_PASSWORD

        pass_response = backend.post('validate', json={'password': password})
        self.assertEqual(pass_response.status_code, 200)

        guid = eval(pass_response.data)['message'][1:]
        otp_response = backend.post(guid, json={})
        self.assertEqual(otp_response.status_code, 400)

    def test_otp_empty(self):
        backend = APP.test_client()
        password = PasswordValidator().VALID_PASSWORD

        pass_response = backend.post('validate', json={'password': password})
        self.assertEqual(pass_response.status_code, 200)

        guid = eval(pass_response.data)['message'][1:]
        otp_response = backend.post(guid, json={'otp': ''})
        self.assertEqual(otp_response.status_code, 401)

    def test_otp_None(self):
        backend = APP.test_client()
        password = PasswordValidator().VALID_PASSWORD

        pass_response = backend.post('validate', json={'password': password})
        self.assertEqual(pass_response.status_code, 200)

        guid = eval(pass_response.data)['message'][1:]
        otp_response = backend.post(guid, json={'otp': None})
        self.assertEqual(otp_response.status_code, 401)

    def _test_otp_(self, guess):
        otp_response = self.backend.post(self.guid, json={'otp': guess})
        if otp_response.status_code > 401:
            raise SystemError  # Test failed because server returns HTTP 500
        return eval(otp_response.data)['result']

    def test_otp_correct(self):
        self.backend = APP.test_client()
        password = PasswordValidator().VALID_PASSWORD

        pass_response = self.backend.post('validate', json={'password': password})
        self.assertEqual(pass_response.status_code, 200)

        self.guid = eval(pass_response.data)['message']

        check_function = self._test_otp_
        guess = _binary_search_timing_attack(check_function, 6)

        # Confirm result
        otp_response = self.backend.post(self.guid, json={'otp': guess})
        self.assertEqual(otp_response.status_code, 200)
        self.assertTrue(eval(otp_response.data)['message'][:4], "CSC{")

    def test_otp_brute_force_incorrect(self):
        self.backend = APP.test_client()
        password = PasswordValidator().VALID_PASSWORD

        pass_response = self.backend.post('validate', json={'password': password})
        self.assertEqual(pass_response.status_code, 200)

        self.guid = eval(pass_response.data)['message']

        check_function = self._test_otp_
        with self.assertRaises(SystemError):
            _brute_force_timing_attack(check_function, 6)


if __name__ == '__main__':
    # Dummy values
    os.environ['flag'] = "CSC{jobs.bankvanbreda.be}"
    os.environ['password'] = "Monkey"

    unittest.main()
