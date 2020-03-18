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

if __name__ =='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)



