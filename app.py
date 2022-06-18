
from flaskext.mysql import MySQL
import pymysql
# from werkzeug import check_password_ha
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from flask_mysqldb import MySQL, MySQLdb

import traceback
import sib_api_v3_sdk

from flask import Flask
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv


app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def home():
    return "Hello"


from routes import validate
from routes import fetch
from routes import attendance

# if __name__ == '__main__':
#     app.run(debug=True)


# app.config['CORS_HEADERS'] = 'Content-Type'

# mysql = MySQL()
# # MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'attribuer'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
# @app.after_request
# def after_request_func(response):
#     """
#         CORS Section
#     """
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add('Access-Control-Allow-Headers', "*")
#     response.headers.add('Access-Control-Allow-Methods', "*")
#     return response


# from flask import Flask, render_template, json, request, redirect
# # pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
# # from flask_mysqldb import MySQL, MySQLdb
# from datetime import datetime
# from flaskext.mysql import MySQL
# import pymysql

# app = Flask(__name__)
# mysql = MySQL()
# # app.secret_key = "caircocoders-ednalan-2020"

# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'attribuer'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)


# @app.route('/')
# def main():
#     return redirect('/useradmin')


if __name__ == '__main__':
    app.run(debug=True)
