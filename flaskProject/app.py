from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from sqlalchemy import delete
import datetime
from sqlalchemy import DateTime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindenszipiszuper.db'
app.config["SECRET_KEY"] = "PEDROPEDROPEDRO"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


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
    valuta = db.Column(db.String, nullable=False)
    type_of_sub = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class ListOfSubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    logo_url = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/mainPage')
@login_required
def main_page():
    return render_template('main.html')


@app.route('/stats_page')
def stats_page():
    return render_template('statistics.html')


@app.route('/input_page')
def input_page():
    listofsubs = ListOfSubs.query.all()
    return render_template('input.html', listofsubs=listofsubs)


@app.route('/registration_page')
def registration_page():
    return render_template('registration_page.html')


@app.route('/profile_page')
def profile_page():
    return render_template('profile.html')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 20:
            flash("Username can only be 20 characters long")
        elif len(username) < 5:
            flash("Username too short!")
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                flash("Username already exists!")
            else:
                user = User(
                    username=username,
                    password=request.form["password"]
                )
                db.session.add(user)
                db.session.commit()
                return render_template("registration_completed.html")
    return render_template("registration_page.html")


# login kódrészlet forrás: https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#define-models

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user:
            if user.password == request.form.get("password"):
                login_user(user)
                return render_template("main.html")
            else:
                flash("Wrong credentials, try again!")
        else:
            flash("Wrong credentials, try again!")

    return redirect(url_for('hello_world'))


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("hello_world"))


@app.route("/addnewsubscription", methods=["GET", "POST"])
def add_new_subscription():
    if request.method == "POST":
        sub = ListOfSubs.query.filter_by(name=request.form.get('subname'))
        if sub:
            new_sub= Subs(
                name=request.form.get('subname'),
                category=request.form.get('subcategory'),
                price=request.form.get('price'),
                valuta=request.form.get('valuta'),
                type_of_sub=request.form.get('subtype'),
                user_id=current_user.id
            )
            add(new_sub)
            if add(new_sub):
                flash("Subscription added successfully!")
            return render_template("input.html")

        elif not request.form.get("subname"):
            flash("Please enter name")
        else:
            new_sub = ListOfSubs(
                name=request.form.get("subname"),
                logo_url=""
            )

            db.session.add(new_sub)

            new_sub = Subs(
                name=request.form.get('subname'),
                category=request.form.get('subcategory'),
                price=request.form.get('price'),
                valuta=request.form.get('valuta'),
                type_of_sub=request.form.get('subtype'),
                user_id=current_user.id
            )

            add(new_sub)
            db.session.commit()
            return render_template("input.html")
    return render_template("input.html")


def add(subscription):
    try:
        if current_user.is_authenticated:
            user=current_user
            user.subscriptions.append(subscription)
            db.session.commit()
            return True
    except Exception as e:
        flash("Something went wrong. Subscription is not added to your profile")
        print(e)
        db.session.rollback()
    return False





# @app.route("/addnewplatform", methods=["GET", "POST"])
# def add_new_platform():
#     if request.method == "POST":
#         temp = request.form.get("subsname")
#         if temp == "Add new platform":
#


if __name__ == '__main__':
    app.run()
