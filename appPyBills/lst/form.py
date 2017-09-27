from flask_wtf import Form
from wtforms import StringField, validators, PasswordField, BooleanField
from wtforms.fields import FloatField
from wtforms.fields.html5 import EmailField
from appPyBills.author.form import RegisterForm
from appPyBills.lst.models import Category
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileAllowed, FileField


class SetupForm(Form):
    name = StringField('Mailbox Name', [validators.DataRequired(), validators.Length(max=80)])
    fullname = StringField('Full Name', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=20)])
    password = PasswordField('New Password', [validators.DataRequired(),
                                              validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    public = BooleanField('Public Mailbox ')


def categories():
    return Category.query


class BillForm(Form):
    pdf = FileField('Bill File (.pdf)', validators=[FileAllowed(['pdf'], 'PDF only!')])
    issuer = StringField('Issuer', validators=[validators.DataRequired(), validators.Length(max=80)])
    due_date = DateField('Due Date', validators=[validators.DataRequired()])
    cat_rel = QuerySelectField('Category', query_factory=categories, allow_blank=True)
    new_category = StringField('New Category')
    amount = FloatField('Amount ($AUD)', validators=[validators.DataRequired()])
