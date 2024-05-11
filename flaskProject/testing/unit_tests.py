import unittest
from datetime import datetime
import pandas as pd
from models import User, Subs, ListOfSubs, BarChart, PieChart, HeatMap
from app import db, app

"""
Ez a .py file az adatbázis adattagjait teszteli, illetve a 3 matplotlibes osztályt.
"""


class TestUser(unittest.TestCase):

    def test_is_authenticated(self):
        user = User(username='test_user', password='password')
        self.assertTrue(user.is_authenticated())

    def test_is_active(self):
        user = User(username='test_user', password='password')
        self.assertTrue(user.is_active())

    def test_is_anonymous(self):
        user = User(username='test_user', password='password')
        self.assertFalse(user.is_anonymous())

    def test_get_id(self):
        user_id = 0
        with app.app_context():
            User.query.filter_by(username='test').delete()
            user = User(username='test', password='test')
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(username='test').first()
            if user:
                user_id = user.id

        self.assertIsInstance(user_id, int)


class TestSubs(unittest.TestCase):

    def test_good_sub(self):
        sub = Subs(
            name="Spotify",
            category="Music",
            price=1800.0,
            start_date=datetime(2024, 1, 22),
            type_of_sub="Monthly",
            user_id=1
        )
        self.assertIsInstance(sub, Subs)
        self.assertEqual(sub.name, 'Spotify')
        self.assertEqual(sub.category, "Music")
        self.assertEqual(sub.start_date, datetime(2024, 1, 22))
        self.assertEqual(sub.type_of_sub, "Monthly")
        self.assertEqual(sub.user_id, 1)

    def test_name_type(self):
        sub = Subs(
            name=123,
            category="Music",
            price=1800.0,
            start_date=datetime(2024, 1, 22),
            type_of_sub="Monthly",
            user_id=1
        )
        self.assertNotIsInstance(sub.name, str)

    def test_category_type(self):
        sub = Subs(
            name='Spotify',
            category=123,
            price=1800.0,
            start_date=datetime(2024, 1, 22),
            type_of_sub="Monthly",
            user_id=1
        )

        self.assertNotIsInstance(sub.category, str)

    def test_price_type(self):
        sub = Subs(
            name="Spotify",
            category="Music",
            price="1800.0",
            start_date=datetime(2024, 1, 22),
            type_of_sub="Monthly",
            user_id=1
        )
        self.assertNotIsInstance(sub.price, float)

    def test_start_date_type(self):
        sub = Subs(
            name="Spotify",
            category="Music",
            price=1800.0,
            start_date=2024,
            type_of_sub="Monthly",
            user_id=1
        )

        self.assertNotIsInstance(sub.start_date, datetime)

    def test_type_of_sub_type(self):
        sub = Subs(
            name="Spotify",
            category="Music",
            price=1800.0,
            start_date=datetime(2024, 1, 22),
            type_of_sub=123,
            user_id=1
        )

        self.assertNotIsInstance(sub.type_of_sub, str)

    def test_user_id_type(self):
        sub = Subs(
            name="Spotify",
            category="Music",
            price=1800.0,
            start_date=datetime(2024, 1, 22),
            type_of_sub="Monthly",
            user_id="abc"
        )

        self.assertNotIsInstance(sub.user_id, int)


class TestListOfSubs(unittest.TestCase):

    def test_good_list_of_subs(self):
        sub = ListOfSubs(
            name="Netflix",
            logo_url=""
        )
        self.assertIsInstance(sub, ListOfSubs)
        self.assertEqual(sub.name, "Netflix")

    def test_name_type(self):
        sub = ListOfSubs(
            name=123,
            logo_url=""
        )

        self.assertNotIsInstance(sub.name, str)

    def test_logo_url_type(self):
        sub = ListOfSubs(
            name="Netflix",
            logo_url=123
        )

        self.assertNotIsInstance(sub.logo_url, str)


class TestBarChart(unittest.TestCase):

    def test_init(self):
        x = ["Game", "Streaming", "Music", "Newspaper"]
        y = [1, 2, 3, 4]
        label = ""
        barchart = BarChart(x, y, label)
        self.assertEqual(barchart.x, x)
        self.assertEqual(barchart.y, y)
        self.assertEqual(barchart.label, label)

    def test_plot_graph(self):
        x = ["Game", "Streaming", "Music", "Newspaper"]
        y = [1, 2, 3, 4]
        label = ""
        barchart = BarChart(x, y, label)
        plot = barchart.plot_graphs()

        self.assertTrue(plot)


class TestData:
    def __init__(self, start_date, price):
        self.start_date = start_date
        self.price = price


class TestPieChart(unittest.TestCase):

    def test_init(self):
        labels = ["Game", "Streaming", "Music", "Newspaper"]
        y = [20, 30, 40, 50]
        piechart = PieChart(y=y, label=labels, x=0)
        plot = piechart.plot_graphs()

        self.assertTrue(plot)


class TestHeatMap(unittest.TestCase):

    def test_query(self):
        self.data = [
            TestData(datetime(2024, 1, 22), 5000),
            TestData(datetime(2024, 9, 7), 6900),
            TestData(datetime(2024, 1, 8), 7000)
        ]
        heatmap = HeatMap(datetime(2024, 1, 1), 2024, self.data)
        dates = [datetime(2024, 1, 22).date(), datetime(2024, 9, 7).date(), datetime(2024, 1, 8).date()]
        dates.sort()
        prices = [7000, 5000, 6900]
        data = heatmap.query_data()
        self.assertIsInstance(data, pd.Series)
        self.assertEqual(list(data.index), dates)
        self.assertEqual(list(data.values), prices)

    def test_plot(self):
        self.data = [
            TestData(datetime(2024, 1, 22), 5000),
            TestData(datetime(2024, 9, 7), 6900),
            TestData(datetime(2024, 1, 8), 7000)
        ]
        heatmap = HeatMap(datetime(2024, 1, 1), 2024, self.data)
        data = heatmap.plot()
        self.assertIsInstance(data, str)


if __name__ == '__main__':
    unittest.main()
