from app import app
import os

# MySQL imports
from flaskext.mysql import MySQL
import pymysql

# Rows from cursors will always be of type dict || cursorclass=DictCursor
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'attribuer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
