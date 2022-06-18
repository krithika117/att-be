from asyncio import constants
from app import app
from flask import Flask, render_template, url_for, request, json, jsonify
# from flaskext.mysql import MySQL
import pymysql
import time
from timeit import default_timer as timer

from flask_cors import CORS, cross_origin
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
# import traceback
import sib_api_v3_sdk
from dotenv import load_dotenv

from config import mysql


@app.route("/viewevent", methods=["POST", "GET"])
def view_event():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    if request.method == 'POST':
        clubChoice = _json['club']
        print(clubChoice)
        cursor.execute(
            "SELECT * FROM events where club=(%s) ORDER BY event ASC", [clubChoice])
        employeelist = cursor.fetchall()
        print(employeelist)
        print('all list')
    return jsonify({'response': employeelist})


@app.route('/createevent', methods=['POST'])
def create_event():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json

    _event = _json['event']
    _date = _json['date']
    _clubChoice = _json['clubChoice']
    _headcount = _json['headcount']

    if _event:

        sql = "INSERT INTO events(eventName,date,clubChoice,headcount) VALUES(%s, %s, %s, %s)"
        data = (_event, _date, _clubChoice, _headcount)
        cursor.execute(sql, data)

        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify({'message': 'User registered successfully'})
        # resp.headers['Access-Control-Allow-Origin'] = '*'

        resp.status_code = 201
        return resp

    else:
        resp = jsonify({'message': 'Bad Request - invalid parameters'})
        resp.status_code = 400
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route("/attendance/club", methods=["POST", "GET"])
def attendance_club():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json

        club = _json['club']
        print(club)

        cursor.execute(
            "SELECT * FROM formdata WHERE serviceClubChoice=(%s) OR techClubChoice1=(%s) OR techClubChoice2=(%s) ORDER BY yearOfStudy,firstName ASC", ([club], [club], [club]))
        employeelist = cursor.fetchall()
        # print(employeelist)

        print('queried')
    return jsonify({'response': employeelist})


@app.route("/attendance/selectmenu", methods=["POST", "GET"])
def attendance_selectmenu():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json

        club = _json['club']
        # query = _json['query']
        print(club)

        cursor.execute(
            "SELECT * FROM events WHERE club=(%s)", ([club]))
        employeelist = cursor.fetchall()
        # print(employeelist)
    return jsonify({'response': employeelist})


@app.route("/attendance/view", methods=["POST", "GET"])
def attendance_view():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json

        club = _json['club']
        query = _json['query']
        print(club)

        cursor.execute(
            "SELECT * FROM attendancetable WHERE club=(%s) AND eventName=(%s)", ([club], [query]))
        employeelist = cursor.fetchall()
        print(employeelist)
        print('queried')
    return jsonify({'response': employeelist})


@app.route("/insert/attendance", methods=["POST", "GET"])
def insert_attendance():
    start = timer()
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json
        data = _json['data']
        _club = _json['club']
        _event = _json['eventName']
        _date = _json['date']

        # to get dict value inside list, use varname[index]['key']
        # ('godevet', '2022-05-06', 'NSS', 'Krithika', '311119205028', 'IT', 'I', '1')

        query_data = [tuple(dic.values()) for dic in data]
        cursor.executemany(
            "INSERT INTO attendancetable(name, regNo, email, department, yearOfStudy, eventName, date, club, attendance) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))", query_data)
        # cursor.execute(sql, data)
        conn.commit()
        cursor.execute(
            "INSERT INTO events(event, date, club) VALUES ((%s),(%s),(%s))", ([_event], [_date], [_club]))
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify({'message': 'User registered successfully'})
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.status_code = 201
        # print(query_data)
        end = timer()
        print("Insertion Time =")
        print(end - start)
        return resp

    return jsonify({'response': 'done'})


@app.route("/update/attendance", methods=["POST", "GET"])
def update_attendance():
    start = timer()
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json
        data = _json['data']
        _club = _json['club']
        _event = _json['eventName']
        # _date = _json['date']

        # to get dict value inside list, use varname[index]['key']
        # 'Krithika', '311119205028', 'ECE', 'IV', '2022-05-06', 'NSS', '1', 'test event'

        query_data = [tuple(dic.values()) for dic in data]
        print("DDATA")
        print(query_data)

        cursor.executemany(
            "UPDATE attendancetable SET attendance=(%s) WHERE eventName=(%s) AND email=(%s) AND club=(%s)", query_data)
        # cursor.execute(sql, data)
        conn.commit()
        print('comm')
        cursor.execute(
            "UPDATE events SET club=(%s) where event=(%s) ", ([_club], [_event]))
        conn.commit()
        print('comm')
        cursor.close()
        conn.close()
        resp = jsonify({'message': 'User registered successfully'})
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.status_code = 201
        end = timer()
        print('Updation Time =', end - start)
        return resp

    return jsonify({'response': 'done'})


@app.route("/attendance/fac/view", methods=["POST", "GET"])
def attendance_fac_view():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json

        club = _json['club']
        q = _json['dept']
        query = _json['query']
        print(club)
        print(query)
        dept = "IT" if q == "dit" else "Mech" if q == "dmech" else "CSE" if q == "dcse" else "EEE" if q == "deee" else "ECE"
        print(dept)
        cursor.execute(
            "SELECT * FROM attendancetable WHERE club=(%s) AND eventName=(%s) AND department=(%s)", ([club], [query], [dept]))
        employeelist = cursor.fetchall()
        print(employeelist)
        print('queried')
    return jsonify({'response': employeelist})


@app.route("/participation/view", methods=["POST", "GET"])
def participation_view():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        _json = request.json

        email = _json['email']
        cursor.execute(
            "SELECT * FROM attendancetable WHERE email=(%s) and attendance='1'", ([email]))
        employeelist = cursor.fetchall()
        print(employeelist)
        print('queried')
    return jsonify({'response': employeelist})


@app.route("/delete/event", methods=["POST", "GET"])
def delete_event():
    start = timer()
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    _json = request.json
    event = _json['event']
    club = _json['club']

    cursor.execute(
        "DELETE FROM attendancetable WHERE eventName=(%s) AND club= (%s)", ([event], [club]))
    conn.commit()
    print('Deleted')
    cursor.execute(
        "DELETE FROM events WHERE event=(%s) AND club= (%s)", ([event], [club]))
    conn.commit()
    print('Deleted')
    cursor.close()
    conn.close()

    end = timer()
    print('Deletion Time = ', end - start)
    return jsonify({'response': 'success'})
