from app import app
from flask import Flask, render_template, url_for, request, json, jsonify
# from flaskext.mysql import MySQL
import pymysql
from timeit import default_timer as timer
from flask_cors import CORS, cross_origin
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
# import traceback
import sib_api_v3_sdk
from dotenv import load_dotenv

from config import mysql


@app.route("/fetchrecords/dept", methods=["POST", "GET"])
def fetchrecords_dept():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json
        test = (_json['email']).split('@')[0]
        dept = ('IT' if test == "dit" else 'CSE' if test == "dcse" else 'ECE'if test == "dece" else 'EEE' if test ==
                "deee" else 'Mech' if test == "dmech" else 'admin')
        print(dept)

        # Department Queries
        if dept != 'admin':
            query2 = _json['query2']
            if query2 == 'all':
                cursor.execute(
                    "SELECT * FROM formdata WHERE department=(%s) ORDER BY firstName, yearOfStudy ASC", [dept])
                employeelist = cursor.fetchall()
                print(employeelist)

            elif query2 != 'all':
                search_text = _json['query2']
                print('wait')
                print(search_text)
                cursor.execute(
                    "SELECT * FROM formdata WHERE department=(%s) AND yearOfStudy=(%s) ORDER BY firstName, yearOfStudy ASC", ([dept], [search_text]))
                employeelist = cursor.fetchall()
                print(employeelist)
                print('queried')
        elif dept == 'admin':
            cursor.execute(
                "SELECT * FROM formdata ORDER BY firstName,yearOfStudy ASC")
            employeelist = cursor.fetchall()
            print('all list')

    return jsonify({'response': employeelist})


@app.route("/fetchrecords/admin", methods=["POST", "GET"])
def fetchrecords_admin():
    start = timer()
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json
        test = (_json['email']).split('@')[0]
        print(test)
        # dept = 'admin'
        # print(dept)
        # Admin Queries

        query1 = _json['query1']
        query2 = _json['query2']
        if query1 == 'all' and query2 == 'all':
            cursor.execute(
                "SELECT * FROM formdata ORDER BY yearOfStudy,firstName ASC")
            employeelist = cursor.fetchall()
            print('all list')
        elif query1 != 'all' and query2 == 'all':
            # search_text = _json['query']
            cursor.execute(
                "SELECT * FROM formdata WHERE department=(%s) ORDER BY firstName, yearOfStudy ASC", [query1])
            employeelist = cursor.fetchall()
            print(employeelist)
        elif query1 == 'all' and query2 != 'all':
            # search_text = _json['query']
            cursor.execute(
                "SELECT * FROM formdata WHERE yearOfStudy=(%s) ORDER BY firstName, yearOfStudy ASC", [query2])
            employeelist = cursor.fetchall()
            print(employeelist)
        elif query1 != 'all' and query2 != 'all':
            cursor.execute(
                "SELECT * FROM formdata WHERE department=(%s) AND yearOfStudy=(%s) ORDER BY firstName, yearOfStudy ASC", ([query1], [query2]))
            employeelist = cursor.fetchall()
            print(employeelist)
        end = timer()
        print("Time =", end - start)
    return jsonify({'response': employeelist})


@app.route("/fetchrecords/club", methods=["POST", "GET"])
def fetchrecords_club():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json
        test = (_json['email']).split('@')[0]
        club = _json['club']
        print(club)
        query1 = _json['query2']
        if query1 == 'all':
            cursor.execute(
                "SELECT * FROM formdata WHERE serviceClubChoice=(%s) OR techClubChoice1=(%s) OR techClubChoice2=(%s) ORDER BY firstName, yearOfStudy ASC", ([club], [club], [club]))
            employeelist = cursor.fetchall()
            print(employeelist)

        elif query1 != 'all':
            search_text = _json['query2']
            print('wait')
            print(search_text)
            cursor.execute(
                "SELECT * FROM formdata WHERE (serviceClubChoice=(%s) OR techClubChoice1=(%s) OR techClubChoice2=(%s)) AND yearOfStudy=(%s) ORDER BY firstName, yearOfStudy ASC", ([club], [club], [club], [search_text]))
            employeelist = cursor.fetchall()
            print(employeelist)
            print('queried')

            print('queried')
    return jsonify({'response': employeelist})
