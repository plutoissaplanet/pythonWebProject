import unittest
import datetime
from flask_login import current_user, login_user, logout_user
from app import app
from flask_testing import TestCase
from models import User
from unittest.mock import MagicMock

"""
TestCasek nagy része https://pythonhosted.org/Flask-Testing/ alapján lettek megírva.
"""


def test_pages(self):
    with self.client:
        user = User.query.filter_by(id=1).first()
        login_user(user)
        current_user.is_authenticated = MagicMock(return_value=True)
        resp = self.client.get('/mainPage')
        self.assertEqual(resp.status_code, 200)
        logout_user()


class TestHelloWorldRoute(TestCase):
    def create_app(self):
        return app

    def test_hello_world(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)


class TestMainPage(TestCase):
    def create_app(self):
        return app

    def test_main_page(self):
        test_pages(self)


class TestStatPage(TestCase):
    def create_app(self):
        return app

    def test_stat_page(self):
        test_pages(self)


class TestInputPage(TestCase):
    def create_app(self):
        return app

    def test_input_page(self):
        test_pages(self)

    def test_input(self):
        user = User.query.filter_by(id=1).first()
        login_user(user)
        current_user.is_authenticated = MagicMock(return_value=True)
        response = self.client.post("/addnewsubscription", data={
            "sub_name": "Disney+",
            "sub_cat": "Streaming",
            "sub_price": 1200,
            "sub_type": "Monthly",
            "sub_date": datetime.datetime(2024, 3, 9),
            "user_id": 1
        })
        self.assertEqual(response.status_code, 302)
        redirected_response = self.client.get(response.headers['Location'])
        self.assertEqual(redirected_response.status_code, 200)
        logout_user()


class TestProfilePage(TestCase):
    def create_app(self):
        return app

    def test_profile_page(self):
        test_pages(self)


class TestRegisterPage(TestCase):
    def create_app(self):
        return app

    def test_registration_page(self):
        test_pages(self)

    def test_registration(self):
        response = self.client.post('/register', data={'username': 'admin', 'password': 'eszter'},
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class TestLoginPage(TestCase):
    def create_app(self):
        return app

    def test_registration_page(self):
        test_pages(self)

    def test_login(self):
        response = self.client.post('/login', data={'username': 'admin', 'password': 'eszter'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(current_user.is_authenticated)
        self.assertEqual(current_user.username, 'admin')


if __name__ == '__main__':
    unittest.main()
