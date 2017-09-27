from appPyBills import db, uploads
from datetime import datetime
from slugify import slugify

class Mailbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('author.id'))  # A foreign key is one that comes from somewhere else.
    is_public = db.Column(db.Boolean)
    public_slug = db.Column(db.String(100), unique=True)
    bills = db.relationship('Bill', backref='mailbox', lazy='dynamic')

    def __init__(self, name, admin, is_public=False):
        self.name = name
        self.admin = admin
        self.is_public = is_public
        self.public_slug=slugify(self.name)

    def __repr__(self):
        return '<Name %r>' % self.name


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mailbox_id = db.Column(db.Integer, db.ForeignKey('mailbox.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    issuer = db.Column(db.String(80))
    slug = db.Column(db.String(256), unique=True)
    post_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    bpay_code = db.Column(db.String(10))
    bpay_acc = db.Column(db.String(25))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    paid = db.Column(db.Boolean)
    amount = db.Column(db.Float)
    cat_rel = db.relationship('Category', backref=db.backref('bill', lazy='dynamic'))
    pdf = db.Column(db.String(255))

    @property
    def pdf_src(self):
        return uploads.url(self.pdf)
    
    def __init__(self, box, author, issuer, due_date, category, amount, pdf=None, bpay_code=None, bpay_acc=None,  paid=False, slug=None, post_date=None):
        # Expects to be passed box and author as objects.
        self.mailbox_id = box.id
        self.author_id = author.id
        self.issuer = issuer
        self.slug = slug
        self.cat_rel = category
        self.pdf=pdf
        if post_date is None:
            self.post_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # format in a way mysql likes
        else:
            self.post_date = post_date
        self.due_date = due_date
        self.paid = paid
        self.bpay_code = bpay_code
        self.bpay_acc = bpay_acc
        self.amount = amount


    def __repr__(self):
        return '<Post %r>' % self.issuer


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name  # This is what makes it work despite no foreign key back the other way, i.e. we have a many:many relationship.
                        # Sort of. Not very well done.


