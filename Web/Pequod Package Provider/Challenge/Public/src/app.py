from flask import Flask, send_from_directory, render_template
from auth import auth_blueprint, token_required, token_optional
from db import init_db, db_session, User, Repository
from api import api_blueprint
from repository import repository_blueprint
from os import getenv, urandom

app = Flask(__name__)
# HA, NO GIGANTIC REQUESTS FOR YOU
app.config['MAX_CONTENT_LENGTH'] = 4*1024*1024
# HA, NO FIXED SECRET KEY FOR YOU
app.secret_key = urandom(32)
init_db()

@app.route("/")
@token_optional # Careful now, don't want to forget to check the users
def home(current_user: User):
    repos = None
    if current_user:
        repos=Repository.get_all_for(current_user)
    return render_template("home.html", current_user=current_user, repos=repos)

@app.route('/.well-known/<path:path>')
def well_knowns(path: str):
    return send_from_directory('.well-known', path)

@app.route("/admin")
@token_required # HA, NO UNGUARDED ROUTE FOR YOU
def admin(current_user: User):
    if str(current_user.id) != str(User.admin().id):
        return "Unauthorized", 401
    return render_template("admin.html", current_user=current_user, flag=getenv("FLAG", "This is supposed to be the flag, but it appears something broke, sorry! If you're running this locally, don't forget to set the FLAG env var, if this is the live challenge, ask an admin for help!"))

app.register_blueprint(api_blueprint)

app.register_blueprint(auth_blueprint)

app.register_blueprint(repository_blueprint)

if __name__ == "__main__":
    app.run()   