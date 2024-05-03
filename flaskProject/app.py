from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from models import User, Subs, ListOfSubs, db, BarChart, PieChart, HeatMap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindenszipiszuper.db'
app.config["SECRET_KEY"] = "PEDROPEDROPEDRO"
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/mainPage')
@login_required
def main_page():
    return render_template('main.html')


@app.route('/stats_page', methods=["GET", "POST"])
def stats_page():
    all_subs = Subs.query.filter_by(user_id=current_user.id).all()

    filtered_subs = []
    cat_label = []
    price_label = []
    method_label = []

    htl = []
    lth = []

    if request.method == "POST":
        used_filters = request.form.getlist('filters')
        for i in range(len(used_filters)):
            if "_cat" in used_filters[i]:
                cat_label.append(used_filters[i].replace("_cat", "").capitalize())
            elif "_price" in used_filters[i]:
                price_label.append(used_filters[i].replace("_price", ""))
            elif "_method" in used_filters[i]:
                method_label.append(used_filters[i].replace("_method", "").capitalize())

            if "highest to lowest_price" in used_filters[i]:
                htl = lowest_highest(all_subs, False)
            if "lowest to highest_price" in used_filters[i]:
                lth = lowest_highest(all_subs, True)

    else:

        used_filters = []

    if cat_label:
        for cat in cat_label:
            filtered_subs.extend(Subs.query.filter_by(user_id=current_user.id, category=cat).all())

    counted_categories = count_subs(subslist=filtered_subs, cats=cat_label)
    graph_bars = BarChart(x=cat_label, y=counted_categories, label="")
    graph_pie = PieChart(y=counted_categories, label=cat_label, x=0)

    plot_url = None
    plot_url2 = None

    if used_filters:
        plot_url = graph_bars.plot_graphs()
        plot_url2 = graph_pie.plot_graphs()

    start_dates = [sub.start_date for sub in all_subs]
    earliest_start_date = min(start_dates)
    heatmap = HeatMap(earliest_start_date, datetime.now().year, all_subs)

    return render_template('statistics.html', all_subs=all_subs, plot_url=plot_url,
                           plot_url2=plot_url2, used_filters=used_filters, cats=cat_label, lth=lth, htl=htl,
                           method_label=method_label, heatmap=heatmap.plot())


def count_subs(subslist, cats):
    nr_gaming = 0
    nr_newspaper = 0
    nr_streaming = 0
    nr_music = 0
    counted_categories = []
    category_list = []

    for subs in subslist:
        category_list.append(subs.category)
        nr_gaming = category_list.count("Gaming")
        nr_newspaper = category_list.count("Newspaper")
        nr_streaming = category_list.count("Streaming")
        nr_music = category_list.count("Music")

    for i in range(len(cats)):
        if cats[i] == "Gaming":
            counted_categories.append(nr_gaming)
        if cats[i] == "Newspaper":
            counted_categories.append(nr_newspaper)
        if cats[i] == "Streaming":
            counted_categories.append(nr_streaming)
        if cats[i] == "Music":
            counted_categories.append(nr_music)

    return counted_categories


def lowest_highest(subs_list, lth):
    lowest_to_highest = sorted(subs_list, key=lambda i: i.price)
    highest_to_lowest = sorted(subs_list, key=lambda i: i.price, reverse=True)

    if lth:
        return lowest_to_highest
    elif not lth:
        return highest_to_lowest


@app.route('/input_page')
def input_page():
    listofsubs = ListOfSubs.query.all()
    usersubs = Subs.query.filter_by(user_id=current_user.id).all()
    return render_template('input.html', listofsubs=listofsubs, usersubs=usersubs)


@app.route('/registration_page')
def registration_page():
    return render_template('registration_page.html')


@app.route('/profile_page', methods=['GET', 'POST'])
def profile_page():
    if request.method == "POST":
        checked_ids = (request.form.getlist("delete"))
        for ids in checked_ids:
            obj = Subs.query.filter_by(id=ids).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return redirect(url_for("profile_page"))

    all_subs=Subs.query.filter_by(user_id=current_user.id).all()
    nr_of_gaming=0
    nr_of_streaming=0
    nr_of_newspaper=0
    nr_of_music=0
    nr_monthly=0
    nr_yearly=0
    nr_onetime=0
    all_numbers=[]

    for subs in all_subs:
        if subs.category == "Gaming":
            nr_of_gaming+=1
        elif subs.category == "Streaming":
            nr_of_streaming += 1
        elif subs.category == "Music":
            nr_of_music += 1

        if subs.category == "Newspaper":
            nr_of_newspaper += 1
        elif subs.type_of_sub == "One time pay":
            nr_onetime+=1
        elif subs.type_of_sub =="Yearly":
            nr_yearly+=1
        elif subs.type_of_sub == "Monthly":
            nr_monthly+=1


    all_numbers.append(nr_of_gaming)
    all_numbers.append(nr_of_streaming)
    all_numbers.append(nr_of_music)
    all_numbers.append(nr_of_newspaper)
    all_numbers.append(nr_onetime)
    all_numbers.append(nr_monthly)
    all_numbers.append(nr_yearly)
    nr_of_subs=len(all_subs)

    price=[subs.price for subs in all_subs]
    dates=[subs.start_date for subs in all_subs]
    max_price=max(price)
    min_price=min(price)
    total=sum(price)
    earliest=min(dates)
    latest=max(dates)



    return render_template('profile.html', nr_of_subs=nr_of_subs, all_numbers=all_numbers, max_price=max_price, min_price=min_price,
                           latest=latest, earliest=earliest, total=total, all_subs=all_subs)


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
        sub_date = request.form.get("sub_start")
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
            type_of_sub=sub_type,
            start_date=datetime.strptime(sub_date, '%Y-%m-%d'),
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
