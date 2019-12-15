from flask import Flask, render_template, request, escape, make_response, redirect, send_from_directory
import random
import time
import re
import uuid
import argon2
import base64
from jinja2 import Markup
import os

app = Flask(__name__,static_folder='static')
app.jinja_env.globals['include_raw'] = lambda filename : escape(app.jinja_loader.get_source(app.jinja_env, filename)[0])


@app.route('/')
def home():
    return render_template('home.html')

users = []
argon2_hash_oma = argon2.argon2_hash(password=str("correcthorsebatterystaple"), salt="XQEXFggkPcw9BtuGkn4ELm4a7r7MUKTjBW2fjaVv6ou8mJ9ZrfEQBYhiGqQ6LzRz", t=16, m=8, p=1, buflen=128, argon_type=argon2.Argon2Type.Argon2_i)
base64_encoded_password = str(base64.b64encode(argon2_hash_oma), "utf-8")
users.append({'username':'oma', 'password_hash': base64_encoded_password, 'salt': 'XQEXFggkPcw9BtuGkn4ELm4a7r7MUKTjBW2fjaVv6ou8mJ9ZrfEQBYhiGqQ6LzRz', 'session': str(uuid.uuid4()) })

argon2_hash_henk = argon2.argon2_hash(password=str("omaisthebest"), salt="QRLKkjpwNTxAEhiBKTAEaUhmhzPzRrZDsghLiNXVShEPAJLHdfJMULzTCDUSHbjL", t=16, m=8, p=1, buflen=128, argon_type=argon2.Argon2Type.Argon2_i)
base64_encoded_password = str(base64.b64encode(argon2_hash_henk), "utf-8")
users.append({'username':'henk', 'password_hash': base64_encoded_password, 'salt': 'QRLKkjpwNTxAEhiBKTAEaUhmhzPzRrZDsghLiNXVShEPAJLHdfJMULzTCDUSHbjL', 'session': str(uuid.uuid4()) })

transactions = [
    {'to':'henk', 'from':'oma', 'amount': '10', 'description': 'Verjaardag 🎂'}
]

@app.route("/get-document/<documentid>")
def get_document(documentid):
    try:
        fileid = base64.b64decode(documentid).decode()
        return send_from_directory("./documents", filename=fileid, as_attachment=True, attachment_filename=documentid)
    except FileNotFoundError:
        abort(404)

@app.route('/document', methods=['GET'])
def document():
    return render_template('document.html')

basket = {
    '1':{
        'description':'Apple Juice',
        'quantity':0
    },
    '2':{
        'description':'Grapefruit Juice',
        'quantity':0
    },
    '3':{
        'description':'Carrot Juice',
        'quantity':0
    },
    '4':{
        'description':'Orange Juice',
        'quantity':0
    },
    '5':{
        'description':'Beet root juice',
        'quantity':0
    }
}

@app.route('/shop', methods=['GET'])
def shop():
    if request.method == 'GET':
        if request.args.get("action") == "buy":
            item = request.args.get("item")
            if item in basket:                
                basket[item]['quantity'] = basket[item]['quantity'] + 1

            baskettotal = 0
            for item in basket:
                baskettotal = baskettotal + basket[item]['quantity']

            return render_template('shop.html', basket = basket, credits=10, baskettotal=baskettotal)
                            
        if request.args.get("action") == "remove":
            item = request.args.get("item")
            if item in basket:
                if basket[item]['quantity'] > 0:
                    basket[item]['quantity'] = basket[item]['quantity'] - 1

            baskettotal = 0
            for item in basket:
                baskettotal = baskettotal + basket[item]['quantity']

            return render_template('shop.html', basket = basket, credits=10, baskettotal=baskettotal)

        if request.args.get("action") == "checkout":
            baskettotal = 0
            order = {}
            for item in basket:
                order[item] = { 'description':basket[item]['description'], 'quantity':basket[item]['quantity'] }                            
                baskettotal = baskettotal + basket[item]['quantity']
                basket[item]['quantity'] = 0
                
            return render_template('checkout.html', basket = order)
                        
    return render_template('shop.html', basket = basket, credits=10, baskettotal=0)



@app.route('/banklogin', methods=['GET','POST'])
def banklogin():
    if request.method == 'GET':
        return redirect("/onlinebanking")

    username = request.form.get('username')
    password = request.form.get('password')
    new_session_value = ''
    current_user = ''
    action_login = True

    for user in users:
        if str(username) == user['username'] and base64.b64decode(user['password_hash']) == argon2.argon2_hash(password=str(password), salt=user['salt'], t=16, m=8, p=1, buflen=128, argon_type=argon2.Argon2Type.Argon2_i):
            new_session_value = str(uuid.uuid4())
            user['session'] = new_session_value
            current_user = user['username']
            action_login = False
            break


    resp = make_response(render_template('onlinebanking.html',transactions = transactions, current_user = current_user, action_login = action_login))
    resp.set_cookie('session-cookie', new_session_value)
    return resp

def getUserFromSession(session):
    username = ''

    for user in users:
        if session == user['session']:
            username = user['username']
            break

    return username

@app.route('/onlinebanking', methods=['GET'])
def onlinebanking():

    action_login = True

    session_cookie = request.cookies.get('session-cookie')
    current_user = getUserFromSession(session_cookie)

    if current_user == 'oma' or current_user == 'henk':
        action_login = False
    else:
        action_login = True

    resp = make_response(render_template('onlinebanking.html',transactions = transactions, current_user = current_user, action_login = action_login))

    return resp

@app.route('/transfer', methods=['POST'])
def transfer():
    to_value = request.form.get('to')
    # from_value = request.form.get('from')
    amount_value = request.form.get('amount')
    description_value = request.form.get('description')

    session_cookie = request.cookies.get('session-cookie')
    current_user = getUserFromSession(session_cookie)

    if current_user != to_value and (to_value == 'henk' or to_value == 'oma'):
        transactions.append({'to':to_value,'from':current_user,'amount':amount_value,'description':description_value})

    return redirect("/onlinebanking")




if __name__ =='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)
    


