import os
import sys
# Set path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #Appends the project directory to sys paths

import unittest
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from appPyBills import app, db

from appPyBills.author.models import *
from appPyBills.lst.models import *


class UserTest(unittest.TestCase):
    def setUp(self):  # Called at the beginning of test

        # We are going to create a database just for testing.
        db_un = app.config['DB_UN']  # Read straight from the config (config.py)
        db_pw = app.config['DB_PASSWORD']
        db_host = app.config['DB_HOST']
        self.db_uri = 'mysql+pymysql://%s:%s@%s/' % (db_un, db_pw, db_host)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Not coming from a browser
        app.config['DB_NAME'] = 'test_db'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['DB_NAME']
        engine=sqlalchemy.create_engine(self.db_uri)
        conn=engine.connect()
        conn.execute('commit')
        conn.execute('CREATE DATABASE '+app.config['DB_NAME'])
        db.create_all()
        conn.close()
        self.app = app.test_client()

    def tearDown(self):  # End of test
        db.session.remove()
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute('commit')
        conn.execute('DROP DATABASE ' + app.config['DB_NAME'])
        conn.close()

    def create_box(self):
        return self.app.post('/setup', data=dict(  # Values to post to form
            name='Test Mailbox',
            fullname='Testy McTesterson',
            email='test@test.test',
            username='Test123',
            password='testpass',
            confirm='testpass',
            public=True
        ), follow_redirects=True)

    def test_create_box(self):  # Test functions have to start with 'test' otherwise unittest won't recognise it.
        rv = self.create_box()
        print(rv.data)
        assert 'Mailbox created.' in str(rv.data)  # This is the flashed message shown on the index page when a mailbox is created.

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects = True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        self.create_box()
        rv = self.login('Test123', 'testpass')
        assert 'User Test123 logged in' in str(rv.data)
        rv = self.logout()
        assert 'User logged out.' in str(rv.data)
        rv = self.login('wrong', 'details')
        assert 'Invalid username/password.' in str(rv.data)

if __name__ == '__main__':
        unittest.main()


