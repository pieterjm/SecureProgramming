from flask import Flask, render_template, request, escape, make_response, redirect, send_from_directory
from jinja2 import Markup
import re
import os
import sys
import time

app = Flask(__name__,static_folder='static')
app.jinja_env.globals['include_raw'] = lambda filename : escape(app.jinja_loader.get_source(app.jinja_env, filename)[0])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/mode', methods=['GET','POST'])
def mode():
    mode = 'Running in normal mode'
    result = None
    if request.method == 'GET':
        return render_template('mode.html',result=None, mode=mode)
    if request.method == 'POST':
        input = request.form.get('input');
        if input != None and re.match("^[A-Za-z0-9]+$",input):
            result = os.system("./util %s" % input)
            if ( result == 512 ):
                mode = 'Running in god mode'
            else:
                time.sleep(3)
            result = len(input)
        else:
            result = None
        return render_template('mode.html',result=result, mode=mode)

@app.route('/error')
def error():
    return render_template('error.html')
        
if __name__ =='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)
    


