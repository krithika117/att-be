from app import app
from flask import Flask, render_template, url_for, request, json, jsonify
# from flaskext.mysql import MySQL
import pymysql

from flask_cors import CORS, cross_origin
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
# import traceback
import sib_api_v3_sdk
from dotenv import load_dotenv

from config import mysql


@app.route('/validate', methods=['POST'])
def validate():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _email = request.form['email']
    # print(_email)
    if _email:
        cursor.execute(
            'SELECT email,isAdmin FROM users WHERE email = %s', (_email))
        user_exist = cursor.fetchone()

        if user_exist:
            if user_exist['isAdmin'] == 0:
                cursor.execute(
                    'SELECT * FROM formdata WHERE email = %s', (_email))
                user_exist1 = cursor.fetchone()
                resp = jsonify(
                    {"message": "exists", "isAdmin": user_exist['isAdmin'], "email": user_exist['email'], "serviceClubChoice": user_exist1['serviceClubChoice'], "techClubChoice1": user_exist1['techClubChoice1'], "techClubChoice2": user_exist1['techClubChoice2']})
                print(resp)
                resp.status_code = 200
                resp.headers['Access-Control-Allow-Origin'] = '*'
            else:
                print(user_exist['isAdmin'])
                resp = jsonify(
                    {"message": "exists", "isAdmin": user_exist['isAdmin'], "email": user_exist['email']})
                resp.status_code = 200
                resp.headers['Access-Control-Allow-Origin'] = '*'
                print('done2')
            return resp

        else:
            resp = jsonify({"message": "clear"})
            resp.status_code = 200
            resp.headers['Access-Control-Allow-Origin'] = '*'
            print('done')
            return resp

    else:
        resp = jsonify({'message': 'Bad Request - invalid parameters'})
        resp.status_code = 400
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp


@app.route('/register', methods=['POST'])
def register():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    print('in')
    _firstName = _json['firstName']
    _lastName = _json['lastName']
    _phoneNumber = _json['phoneNumber']
    _email = _json['email']
    _rollNo = _json['rollNo']
    _regNo = _json['regNo']
    _department = _json['department']
    _yearOfStudy = _json['yearOfStudy']
    _serviceClubChoice = _json['serviceClubChoice']
    _techClubChoice1 = _json['techClubChoice1']
    _techClubChoice2 = _json['techClubChoice2']

    if _email:

        sql = "INSERT INTO formdata(firstName,lastName,phoneNumber,email,rollNo,regNo,department,yearOfStudy,serviceClubChoice,techClubChoice1,techClubChoice2) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (_firstName, _lastName, _phoneNumber, _email, _rollNo, _regNo,
                _department, _yearOfStudy, _serviceClubChoice, _techClubChoice1, _techClubChoice2)
        cursor.execute(sql, data)
        sql1 = "INSERT INTO users(email,isAdmin) VALUES(%s,%s)"
        data1 = (_email, 0)
        cursor.execute(sql1, data1)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify({'message': 'User registered successfully'})
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        sendMail(_firstName, _email, _serviceClubChoice,
                 _techClubChoice1, _techClubChoice2)
        resp.status_code = 201
        return resp

    else:
        resp = jsonify({'message': 'Bad Request - invalid parameters'})
        resp.status_code = 400
        # resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


def sendMail(firstName, email, serviceClubChoice, techClubChoice1, techClubChoice2):
    print("Sending Mail tp " + email)
    # print(firstName)
    # print(email)
    # print(serviceClubChoice)
    # print(techClubChoice1)
    # print(techClubChoice2)

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'

 # create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{
            "email": email,
            "name": firstName}],
        template_id=1,
        params={
            "firstName": firstName,
            "serviceClubChoice": serviceClubChoice,
            "techClubChoice1": techClubChoice1,
            "techClubChoice2": techClubChoice2,
        },
        headers={
            "X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
            "charset": "iso-8859-1"
        }
    )  # SendSmtpEmail | Values to send a transactional email

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
        print('sent')
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        print('error')


@app.route("/delete_user", methods=["POST"])
def delete_user():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    email = _json['emailDeletion']
    cursor.execute("DELETE FROM users WHERE email = (%s)", [email])
    cursor.execute("DELETE FROM formdata WHERE email = (%s)", [email])
    conn.commit()
    cursor.close()
    conn.close()
    print('Done')
    return jsonify({'response': 'success'})
