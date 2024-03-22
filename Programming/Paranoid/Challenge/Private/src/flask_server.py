import logging
import os
import time
from uuid import uuid4

from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS

from otp_manager import OTPManager
from password_validator import PasswordValidator


def get_login_page() -> str:
    with open('index.html') as html_file:
        html_list = html_file.readlines()
    login_html = "".join(html_list)
    return login_html


APP = Flask(__name__)
CORS(APP)
OTP_MANAGER = OTPManager()
LOGIN_PAGE = get_login_page()

@APP.route('/')
def default_route():
    return redirect(url_for('login_page'))

@APP.route('/login')
def login_page():
    return LOGIN_PAGE


@APP.route('/validate', methods=['POST'])
def process_password():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        if 'password' not in data:
            return jsonify({'error': 'Password not provided'}), 400

        # Extract the input string
        guess = data['password']

        # Check password
        start_time = time.time()
        result = PasswordValidator().check_password(guess)
        end_time = time.time()

        if result == 0:
            http_code = 200
            guid = str(uuid4())
            message = f"/{guid}"
            OTP_MANAGER.enable_otp(guid)
        else:
            http_code = 401
            message = "Wrong password!"
        return jsonify({
            "result": result,
            "message": message,
            "took": end_time - start_time
        }), http_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@APP.route('/<guid>', methods=['POST'])
def process_otp(guid):
    try:
        # Check if GUID is registered with an OTP
        is_active = OTP_MANAGER.check_otp_active(guid)
        if not is_active:  # If this guid does not correspond to an active OTP session
            return jsonify({'error': 'endpoint not found'}), 404

        # Get the JSON data from the request
        data = request.get_json()
        if 'otp' not in data:
            return jsonify({'error': 'OTP not provided'}), 400

        # Extract the input string
        guess = data['otp']

        # Register attempt
        OTP_MANAGER.update_otp_counter(guid)
        # Check password
        start_time = time.time()
        result = OTP_MANAGER.check_otp(guess, guid)
        end_time = time.time()

        if result == 0:
            http_code = 200
            message = os.environ['flag']
        else:
            http_code = 401
            message = f"Invalid OTP. Tries left: {OTP_MANAGER.ACTIVE_OTP_TRIES[guid] if guid in OTP_MANAGER.ACTIVE_OTP_TRIES else 0 }"
        return jsonify({
            "result": result,
            "message": message,
            "took": end_time - start_time
        }), http_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    APP.run(debug=True, port=80)
