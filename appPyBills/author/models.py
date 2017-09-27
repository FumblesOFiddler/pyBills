from appPyBills import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(35), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    is_auth = db.Column(db.Boolean)
    bills = db.relationship('Bill', backref='author', lazy='dynamic')

    def __init__(self, fullname, email, username, password, is_auth=False):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.is_auth = is_auth

    def __repr__(self):
        return '<Author %r>' % self.username
