from app import app
import os

# MySQL imports
from flaskext.mysql import MySQL
import pymysql

# Rows from cursors will always be of type dict || cursorclass=DictCursor
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'sql6500670'
app.config['MYSQL_DATABASE_PASSWORD'] = 'yU7PirIPHl'
app.config['MYSQL_DATABASE_DB'] = 'sql6500670'
app.config['MYSQL_DATABASE_HOST'] = 'sql6.freemysqlhosting.net'
mysql.init_app(app)
