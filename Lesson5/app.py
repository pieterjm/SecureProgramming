from flask import Flask, render_template, request, escape, make_response, redirect, send_from_directory
from jinja2 import Markup
import hashlib
import sys
import re

app = Flask(__name__,static_folder='static')
app.jinja_env.globals['include_raw'] = lambda filename : escape(app.jinja_loader.get_source(app.jinja_env, filename)[0])

pwhash = '4e63e90dfb63a150e9b81f1e60f548d080c142d9162015154f47c19ab1475048'
          
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('loginform.html', result = None)
    if request.method == 'POST':
        try:
            hash = hashlib.sha256(request.form.get('password').encode()).hexdigest()
            print(hash, file=sys.stderr)
            if hash == pwhash:
                print("equal", file=sys.stderr)
                return render_template('loggedin.html')
            else:
                return render_template('loginform.html', result = 'Invalid login')        
        except:
            return render_template('loginform.html', result = 'Invalid login')

@app.route('/decode', methods = ['GET','POST'])
def decode():
    if request.method == 'GET':
        return render_template('encoded.html', result = None)
    if request.method == 'POST':
        key = request.form.get('key')
        data = request.form.get('data')
               
        if key != None and re.match("^[A-Za-z]{26}$",str(key)):
            key = str(key).upper()
            if data != None:
                decoded = ""
                data = str(data)
                for c in data:
                    if re.match("^[A-Za-z]$",c):
                        decoded += key[ord(c.upper()) - 65]
                    else:
                        decoded += c
                return render_template('encoded.html', result = decoded)
            else:
                return render_template('encoded.html', result = 'Invalid data')
        else:
            return render_template('encoded.html', result = 'Invalid key')

if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')


