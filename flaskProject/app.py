import random
import base64
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from matplotlib.figure import Figure
import numpy as np

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


class Graphs:
    def __init__(self, x, y, label):
        self._x = x
        self._y = y
        self._label = label

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    def coloring(self, param):
        colors = ["#00897B", "#32A27F", "#5EBA7D", "#8CD178", "#C0E673", "#F9F871",
                  "#746BBB", "#A558A1"]
        nr_needed = len(param)
        selected_colors = random.sample(colors, k=nr_needed)
        return selected_colors

    def customize_axes(self, ax):
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines[['right', 'top']].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')


class BarChart(Graphs):
    def __init__(self, x, y, label):
        super().__init__(x, y, label)

    def set_data(self, x, y):
        self.x = x
        self.y = y

    def set_label(self, label):
        self.label = label

    def plot_graphs(self):
        fig = Figure()
        ax = fig.subplots()
        ax.bar(self.x, self.y, color=self.coloring(self.x))
        self.customize_axes(ax)
        buf = BytesIO()
        fig.savefig(buf, format="png", transparent=True)
        data = base64.b64encode(buf.getvalue()).decode("ascii")
        return data


class PieChart(Graphs):
    def __init__(self, x, y, label):
        super().__init__(x, y, label)

    def plot_graphs(self):
        fig = Figure()

        self.y = np.array(self.y).flatten()
        ax = fig.subplots()
        ax.pie(self.y, labels=self.label, colors=self.coloring(self.y),
               wedgeprops=dict(width=0.3, edgecolor='w'),
               textprops={'color': "w"},
               autopct=lambda pct: f"({int(pct / 100 * sum(self.y))})")

        buf = BytesIO()
        fig.savefig(buf, format="png", transparent=True)
        data = base64.b64encode(buf.getvalue()).decode("ascii")
        return data


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
    usersubs = Subs.query.filter_by(user_id=current_user.id, valuta="HUF").all()
    counted_categories = count_subs(usersubs)
    graph_bars = BarChart(x=["Gaming", "Newspaper", "Streaming", "Music"],
                          y=counted_categories, label="")
    graph_pie = PieChart(y=[counted_categories],
                         label=["Gaming", "Newspaper", "Streaming", "Music"], x=0)
    return render_template('statistics.html', usersubs=usersubs, plot_url=graph_bars.plot_graphs(),
                           plot_url2=graph_pie.plot_graphs())


def count_subs(subslist):
    nr_gaming = 0
    nr_newspaper = 0
    nr_streaming = 0
    nr_music = 0
    category = []
    counted_categories = []
    for subs in subslist:
        category.append(subs.category)
        nr_gaming = category.count("Gaming")
        nr_newspaper = category.count("Newspaper")
        nr_streaming = category.count("Streaming")
        nr_music = category.count("Music")
    counted_categories.append(nr_gaming)
    counted_categories.append(nr_newspaper)
    counted_categories.append(nr_streaming)
    counted_categories.append(nr_music)
    return counted_categories


@app.route('/input_page')
def input_page():
    listofsubs = ListOfSubs.query.all()
    usersubs = Subs.query.filter_by(user_id=current_user.id).all()
    return render_template('input.html', listofsubs=listofsubs, usersubs=usersubs)


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


# login kódrészlet forrás:
# https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/
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
        sub_name = request.form.get('subname')
        if not sub_name:
            flash("Please enter the name of your subscription!")
        sub_cat = request.form.get('subcategory')
        sub_price = request.form.get('price')
        if not sub_price:
            flash("Please enter the price of your subscription")
        else:
            try:
                sub_price = float(sub_price)
            except ValueError:
                flash("Please enter a valid price")
                return render_template("input.html")

        sub_valuta = request.form.get('valuta')
        sub_type = request.form.get('subtype')

        existingsub = ListOfSubs.query.filter_by(name=sub_name).one_or_none()

        if existingsub is None:
            new_sub = ListOfSubs(
                name=sub_name,
                logo_url=""
            )
            db.session.add(new_sub)

        new_sub = Subs(
            name=sub_name,
            category=sub_cat,
            price=sub_price,
            valuta=sub_valuta,
            type_of_sub=sub_type,
            user_id=current_user.id
        )
        add(new_sub)
        db.session.commit()
        flash("Subscription added successfully!")

    usersubs = Subs.query.filter_by(user_id=current_user.id).all()

    return render_template("input.html", usersubs=usersubs)


def add(subscription):
    try:
        if current_user.is_authenticated:
            user = current_user
            user.subscriptions.append(subscription)
            return True
    except Exception as e:
        flash("Something went wrong. Subscription is not added to your profile")
        print(e)
        db.session.rollback()
    return False


if __name__ == '__main__':
    app.run()
