from flask import Flask, render_template, request, redirect, url_for, flash, session
import hashlib
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(64)

flag = os.environ.get(
    "FLAG", "There is an issue with the flag. Please contact the admin."
)

# Dictionary to store user data
users = {}

competitions = [
    {
        "id": 1,
        "name": "National Badminton Championship",
        "date": "2023-04-15",
        "location": "New York, NY",
        "description": "Annual national championship for badminton players.",
    },
    {
        "id": 2,
        "name": "International Badminton Open",
        "date": "2023-06-20",
        "location": "London, UK",
        "description": "International tournament featuring top badminton players.",
    },
    {
        "id": 3,
        "name": "Cyber Security Badminton Cup",
        "date": "2024-03-23",
        "location": "Brussels, Belgium",
        "description": "Only for tryharders",
    },
    {
        "id": 4,
        "name": "Exotic Bamboo Cup",
        "date": "2023-09-05",
        "location": "Brussels, Belgium",
        "description": "An unusual badminton competition played on courts made of bamboo.",
    },
    {
        "id": 5,
        "name": "Cherry Blossom Badminton Challenge",
        "date": "2023-10-12",
        "location": "Antwerp, Belgium",
        "description": "A badminton tournament held amidst blooming cherry blossom trees for added ambiance.",
    },
    {
        "id": 6,
        "name": "Belgian Chocolate Shuttle Smash",
        "date": "2023-11-20",
        "location": "Bruges, Belgium",
        "description": "Players compete while enjoying Belgium's finest chocolates and delicacies.",
    },
    {
        "id": 7,
        "name": "Foggy Forest Badminton Challenge",
        "date": "2024-01-08",
        "location": "Ardennes, Belgium",
        "description": "A badminton tournament held deep in the misty forests of the Ardennes.",
    },
    {
        "id": 8,
        "name": "Diamond Shuttle Showdown",
        "date": "2024-03-17",
        "location": "Antwerp, Belgium",
        "description": "Players compete for a shuttlecock encrusted with precious diamonds.",
    },
    {
        "id": 9,
        "name": "Brussels Waffle Open",
        "date": "2024-05-10",
        "location": "Brussels, Belgium",
        "description": "A badminton tournament where players enjoy delicious Belgian waffles during breaks.",
    },
    {
        "id": 10,
        "name": "Grand Canal Badminton Cruise",
        "date": "2024-06-28",
        "location": "Bruges, Belgium",
        "description": "A unique badminton tournament held on a cruise ship along Belgium's picturesque canals.",
    },
    {
        "id": 11,
        "name": "Rooftop Racket Rally",
        "date": "2024-08-15",
        "location": "Brussels, Belgium",
        "description": "Players compete atop iconic Brussels rooftops with stunning city views.",
    },
    {
        "id": 12,
        "name": "Windmill Shuttle Showdown",
        "date": "2024-10-05",
        "location": "Bruges, Belgium",
        "description": "A badminton tournament held near historic windmills, blending tradition with sport.",
    },
    {
        "id": 13,
        "name": "Ghent Grapes Gala",
        "date": "2024-11-18",
        "location": "Ghent, Belgium",
        "description": "A badminton tournament featuring Belgium's finest grapes and wines for players to enjoy.",
    },
    {
        "id": 14,
        "name": "Aurora Shuttle Spectacle",
        "date": "2025-01-12",
        "location": "Ardennes, Belgium",
        "description": "Players compete under the mesmerizing glow of the Northern Lights in the Ardennes.",
    },
    {
        "id": 15,
        "name": "Golden Fries Badminton Classic",
        "date": "2025-03-20",
        "location": "Brussels, Belgium",
        "description": "A prestigious badminton tournament held in celebration of Belgium's famous golden fries.",
    },
]


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Hash the password with SHA-512
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        if username in users and users[username]["password"] == hashed_password:
            session["username"] = username
            session["role"] = users[username][
                "role"
            ]  # Set the user's role in the session
            flash("Login successful.")
            return redirect(url_for("home"))
        flash("Invalid username or password.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("role", None)
    flash("Logged out successfully.")
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form.get(
            "role", "user"
        )  # Get the selected role, default to 'user' if not set

        # Check if username or password is empty
        if not username or not password:
            flash("Username and password cannot be empty.")
            return redirect(url_for("register"))

        # Hash the password with SHA-512
        hashed_password = hashlib.sha512(password.encode()).hexdigest()

        if username in users:
            flash("Username already exists.")
            return redirect(url_for("register"))

        # Check if the role exists
        valid_roles = ["user", "admin"]  # Define valid roles
        if role not in valid_roles:
            flash("Invalid role.")
            return redirect(url_for("register"))

        users[username] = {
            "password": hashed_password,
            "role": role,
        }  # Store the hashed password and role
        flash("Registration successful.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/")
def home():
    if "username" not in session:
        flash("You must be logged in to view this page.")
        return redirect(url_for("login"))
    return render_template("home.html", competitions=competitions)


@app.route("/manage-competitions")
def manage_competitions():
    global flag
    if "username" not in session or "role" not in session or session["role"] != "admin":
        flash("You do not have permission to access this page.")
        return redirect(url_for("home"))
    return render_template("manage_competitions.html", flag=flag)
