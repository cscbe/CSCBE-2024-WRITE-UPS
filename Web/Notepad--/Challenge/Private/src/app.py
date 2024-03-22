from datetime import datetime
from uuid import uuid1
from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import db_session, init_db
from models import User, Note

from bot import Bot

app = Flask(__name__)
app.secret_key = "SBBi5wVj6ReUSLAioqB7"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

init_db()

@login_manager.user_loader
def load_user(id):
    return db_session.query(User).get(int(id))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    page = 'login'
    if request.method == 'POST':
        print(request.form)
        user = db_session.query(User).filter_by(username=request.form['username']).first()
        if user == None or request.form['password'] != user.password:
            error = 'Invalid login information'
        else:
            session['logged_in'] = True
            
            if user.username == 'admin':
                session['admin'] = True
            else:
                session['admin'] = False
            
            login_user(user)
            return redirect(url_for('notes_list'))
    return render_template('login.html', error=error, page=page)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    page = 'register'
    if request.method == 'POST':
        user_check = db_session.query(User).filter_by(username=request.form['username']).first()
        if user_check != None:
            error = 'User name already taken, please choose another one'
        else:
            session['logged_in'] = True
            user = User(username=request.form['username'], password=request.form['password'])
            db_session.add(user)
            db_session.commit()
            login_user(user)
            flash('Thanks for signing up, you are now logged in')
            return redirect(url_for('notes_list'))
    return render_template('register.html', error=error, page=page)


@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('login'))


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("notes_list"))


@app.route("/notes", methods=["GET"])
@login_required
def notes_list():
    notes = db_session.query(Note).where(Note.author == current_user).all()
    return render_template("notes_list.html", notes=notes)


@app.route("/notes/new", methods=["GET", "POST"])
@login_required
def new_note():
    if request.method == "GET":
        return render_template("new_note.html")
    
    uuid = uuid1(node=171701900198059, clock_seq=current_user.id)
    title = request.form["title"]
    content = request.form["content"]
    created = datetime.now()
    author = current_user
    
    note = Note(id=str(uuid), title=title, content=content, created=created, author=author)
    db_session.add(note)
    db_session.commit()
    
    return redirect(url_for("view_note", uuid=uuid))


@app.route("/notes/view", methods=["GET"])
@login_required
def view_note():
    uuid = request.args.get("uuid", default="", type=str)
    note = db_session.query(Note).filter_by(id=uuid).first()
    
    if note is None:
        return redirect(url_for("notes_list"))
    
    usernames = [user.username for user in db_session.query(User).all()]
    
    return render_template("view_note.html", note=note, usernames=usernames)


@app.route("/notes/share", methods=["POST"])
@login_required
def share_note():
    uuid = request.form["uuid"]
    username = request.form["username"]
    
    note = db_session.query(Note).filter_by(id=uuid).first()
    user = db_session.query(User).filter_by(username=username).first()
    
    if note is None:
        return render_template("share_note.html", custom_error=f"Note {uuid} not found.")
    
    if user is None:
        return render_template("share_note.html", custom_error=f"User {username} not found.")
    elif username == 'admin':
        Bot(uuid)
    else:
        return render_template("share_note.html", custom_error=f"As we received multiple complaints with this functionnality, you can only share your notes with admin for now.")
        
    return render_template("share_note.html", uuid=uuid, username=username)


@app.route("/logs", methods=["GET"])
@login_required
def logs():
    if not session.get("admin"):
        return redirect(url_for("notes_list"))
    
    notes = db_session.query(Note).limit(100).all()
    return render_template("logs.html", notes=notes)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
