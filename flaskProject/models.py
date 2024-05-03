import random
import base64
from io import BytesIO
import io
from matplotlib.figure import Figure
import numpy as np
from flask_sqlalchemy import SQLAlchemy
import calplot
import pandas as pd
import matplotlib

matplotlib.use('TkAgg')

db = SQLAlchemy()


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
    start_date = db.Column(db.DateTime, nullable=False)
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

    """
    Ez a lenti HeatMap rész össze lett ollózva különböző oldalakról. Saját módosításokat kellett még
    végeznem rajta, de javarészt netről van.

    Heatmap generálása. A query_data function összeszámolja a napi költéseket és a spent_on_days dict-be rakja,
    ahol a key a dátum. A total_spending a színezéshez szükséges.
    
    A plot() pedig magát a figuret plotolja.
    """

class HeatMap:

    def __init__(self, earliest_date, year, data):
        self.earliest_date = earliest_date
        self.spent_on_days = {}
        self._year = year
        self._data = data

    def query_data(self):
        for dat in self._data:
            date = dat.start_date.date()
            if date in self.spent_on_days:
                self.spent_on_days[date] += dat.price
            else:
                self.spent_on_days[date] = dat.price

        dates = sorted(self.spent_on_days.keys())
        total_spending = [self.spent_on_days[date] for date in dates]
        final_data = np.array(total_spending)
        final_final_data = pd.Series(final_data, index=dates)
        return final_final_data

    def plot(self):
        datas = self.query_data()
        datas.index = pd.to_datetime(datas.index)
        fig, ax = calplot.calplot(data=datas, cmap='inferno', colorbar=True)
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', transparent=True)
        buffer.seek(0)
        heatmap = base64.b64encode(buffer.getvalue()).decode()

        return heatmap
