from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindenszipiszuper.db'
app.config["SECRET_KEY"] = "PEDROPEDROPEDRO"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    subscriptions = db.relationship('Subs', backref='user', lazy=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Subs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    type_of_sub = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/mainPage')
def main_page():
    return render_template('main.html')


@app.route('/statsPage')
def stats_page():
    return render_template('statistics.html')


@app.route('/inputPage')
def input_page():
    return render_template('input.html')


@app.route('/registration_page')
def registration_page():
    return render_template('registration_page.html')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return render_template("registration_completed.html")
    else:
        return "Stg went wrong"


# login kódrészlet forrás: https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#define-models

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()

        if user.password == request.form.get("password"):
            login_user(user)
            return render_template("main.html")

    return "Stg went wrong"


if __name__ == '__main__':
    app.run()
