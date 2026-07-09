from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from database import db, User, Chat
from chatbot import get_response
from flask import jsonify

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("chat"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing = User.query.filter_by(email=email).first()

        if existing:
            flash("Email already exists")
            return redirect(url_for("register"))

        user = User(
            username=username,
            email=email
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(user)

            return redirect(url_for("chat"))

        flash("Invalid Email or Password")

    return render_template("login.html")

@app.route("/chat")
@login_required
def chat():

    chats = Chat.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "chat.html", 
        username=current_user.username,
        chats=chats
    )


@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully")

    return redirect(url_for("login"))


@app.route("/send_message", methods=["POST"])
@login_required
def send_message():

    data = request.get_json()

    message = data.get("message", "")

    reply = get_response(message)

    chat = Chat(
        user_id=current_user.id,
        message=message,
        reply=reply
    )

    db.session.add(chat)
    db.session.commit()

    return jsonify({
        "reply": reply
    })


@app.route("/clear_chat")
@login_required
def clear_chat():

    Chat.query.filter_by(user_id=current_user.id).delete()

    db.session.commit()

    flash("Chat cleared successfully.")

    return redirect(url_for("chat"))
    

if __name__ == "__main__":
    app.run(debug=True)