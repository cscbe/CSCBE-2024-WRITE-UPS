from functools import wraps
import jwt
from flask import request, Request, Blueprint, request, redirect, make_response, url_for, render_template
from db import db_session, User
import urllib
from urllib.parse import urlparse
import json

token_private_key_json = json.load(open("private-key.json"))
token_private_key_jwk = jwt.PyJWK(token_private_key_json)

def token_optional(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = check_token(request)
        return f(*args, current_user=current_user, **kwargs)

    return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = check_token(request)
        if current_user is None:
            return redirect(url_for("auth.logout"))
        return f(*args, current_user=current_user, **kwargs)

    return decorated

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            error = "Missing field"
        else:
            user = User.from_username(request.form['username'])

            if user != None:
                # HA! NO USER OVERWRITING FOR YOU
                error = 'Username is already in use'
            else:
                user = User.new(request.form['username'], request.form['password'])
                response = make_response(redirect(url_for('home')))
                response.set_cookie("Authorization", make_token(user))
                return response
    return render_template('signup.html', error=error)

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        user = User.from_username(request.form['username'])
        if user == None:
            error = 'Invalid login'
        elif not user.compare_passwords(request.form['password']):
            error = 'Invalid login'
        else:
            response = make_response(redirect(url_for('home')))
            response.set_cookie("Authorization", make_token(user))
            return response
    return render_template('login.html', error=error)

@auth_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    response = make_response(redirect(url_for('home')))
    response.delete_cookie("Authorization")
    return response

@auth_blueprint.route("/user", methods=["GET"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def user_settings(current_user: User):
    return render_template('user.html', user=current_user)

@auth_blueprint.route("/user", methods=["POST"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def update_user(current_user: User):
    if not request.form['old_password'] or not request.form['new_password']:
        return render_template('user.html', user=current_user, error="Missing password field")
    
    # HA, NO PASSWORD RESET ABUSE FOR YOU
    if not current_user.compare_passwords(request.form['old_password']):
        return render_template('user.html', user=current_user, error="Invalid password")
    
    current_user.update_password(request.form['new_password'])
    
    return redirect(url_for('home')), 200

@auth_blueprint.route("/user", methods=["DELETE"])
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def delete_user(current_user: User):
    current_user.delete()
    return redirect(url_for("auth.logout"))


def make_token(user: User):
    return jwt.encode(
        {"iss": "http://pequod_package_provider.challenges.cybersecuritychallenge.be", "sub": user.id},
        key=token_private_key_jwk.key,
        headers={"jku": "http://localhost/.well-known/jwks.json", "kid": "mykey"},
        algorithm="RS256",
    )

def check_token(request: Request):
    token = None
    if "Authorization" in request.headers:
        # AS IF
        token = request.headers["Authorization"].split(" ")[1]
    if "Authorization" in request.cookies:
        token = request.cookies.get("Authorization")
    if not token:
        return None
    try:
        h = jwt.get_unverified_header(token)
        # DID YOU REALLY THINK THIS WOULD WORK?
        if h.get("alg") == "None" or h.get("alg") == None:
            raise Exception("HA! NO ALG BYPASS FOR YOU!")

        if h.get("typ") != "JWT":
            raise Exception("the hell is this")

        if h.get("jku"):
            jku = urlparse(h.get("jku"))
            if jku.scheme.lower() == "https" or jku.port != None:
                raise Exception("HA! NO REMOTE JKU FOR YOU!")
            elif jku.scheme.lower() == "http" and (jku.netloc != "localhost" or not str(jku.path).endswith(".json")):
                raise Exception("HA! NO REMOTE JKU FOR YOU!")

        # THIS FALLBACK, IS MY FALLBACK, NO ARBITRARY FALLBACKS FOR YOU!
        c = jwt.PyJWKClient(h.get("jku") or "http://localhost/.well-known/jwks.json")
        k = c.get_signing_key_from_jwt(token)
        data = jwt.decode(
            token,
            k.key,
            algorithms=["RS256"],  # HA! NO ALG BYPASS FOR YOU!
        )

        # Since we checked everything before then, NO IDOR FOR YOU!
        current_user: User = User.from_id(data['sub'])
        if current_user is None:
            return None
    except Exception as e:
        return None

    return current_user