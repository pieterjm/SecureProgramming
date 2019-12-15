from flask import Flask, render_template, request, escape, make_response, redirect
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


orderstatus = [
    "Shipping",
    "In customs",
    "Processing order",
    "Payment stalled",
    "Missing, but we think we know were it is",
    "Missing, no clue where to search",
    "Order not found",
    "Pending",
    "In queue",
    "Awaiting payment",
    "Awaiting fulfillment",
    "Awaiting shipment",
    "Awaiting pickup",
    "Completed",
    "Shipped",
    "Cancelled",
    "Refunded",
    "Disputed",
    "Forged",
    "Hacked",
    "Fixed",
    "Manual verification required",
    "Partially refunded",
    "Not refunded",
    "Gone with the wind",
    "No clue",
    "Awaiting search result",
    "Ehhhh"
    ]

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/trackorder', methods=['GET'])
def trackorder():
    if request.method == 'GET':
        r = random.randrange(1,20)
        return render_template('trackorder.html',orderid = request.args.get('orderid'), orderstatus = orderstatus[random.randrange(0,len(orderstatus))])
    else:
        return render_template('trackorder.html',orderid = None, orderstatus = orderstatus[random.randrange(0,len(orderstatus))])

comments = [
    {'user':'Calvin','comment':'My lawyers checked it carefully and concluded that Craig is Satoshi.'},
    {'user':'Peter','comment':'CSW is a fraud! See you in court!'}
]

@app.route('/blog', methods=['GET','POST'])
def blog():
    if request.method == 'GET':
        return render_template('blog.html',comments = comments)

    comment = request.form.get('comment')
    user = request.form.get('user')

    # remove all html tags from the comment and the user in order to prevent XSS
    comment = re.sub(r"\<[a-zA-Z][^\<\>]*>",'',comment)
    user = re.sub(r"\<[a-zA-Z][^\<\>]*>",'',user)

    comments.append({'user':user,'comment':comment})

    return render_template('blog.html', comments = comments)


@app.route('/profile',  methods=['GET','POST'])
def profile():
    return render_template('profile.html')

@app.route('/timer', methods=['GET'])
def timer():
    timer = request.args.get('timer')
    if timer:
        return render_template('timer.html', timer = timer )
    else:
        return render_template('settimer.html')

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



