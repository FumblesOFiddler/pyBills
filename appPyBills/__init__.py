from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, ALL
# Flask
app = Flask(__name__)
app.config.from_object('settings')

bcrypt = Bcrypt(app)  #Initialize bcrypt for password hashing

# Models
db = SQLAlchemy(app)

# Migration
migrate = Migrate(app, db)

# uploads
uploads = UploadSet('billpdfs', ALL)
configure_uploads(app, uploads)

# This looks shit but they need to be down here because they depend on the above declarations.
# Whalan has advised you not to use alchemy. Remember that/prostrate yourself for next time.
from appPyBills.lst import views
from appPyBills.author import views


