from base64 import b64encode
from os import urandom
# random_bytes = urandom(64)
# token = b64encode(random_bytes).decode('utf-8')

# Settings - Flask
SECRET_KEY = 'ASDKJFHKJKSHAJKSDHJFHASDF'
DEBUG = True

# Settings - MySQL
DB_UN = 'root'
DB_PASSWORD = 'dicks420'
DB_NAME = 'bills'
DB_HOST = 'localhost'
DB_URI = 'mysql+pymysql://%s:%s@%s/%s' % (DB_UN, DB_PASSWORD, DB_HOST, DB_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True  # Make that god damn error message go away

# Uploads
UPLOADS_DEFAULT_DEST = 'E:/Jim/Python Projects/PyBills/appPyBills/static/'
UPLOADS_DEFAULT_URL = '/static/' # needs a trailing slash
