from flask import Flask, render_template, request, escape, make_response, redirect, send_from_directory
import random
import time
import re
import uuid
import base64
import subprocess
import json
import sqlite3
from jinja2 import Markup
import sys
import xmlschema
import os

xmlschema.limits.MAX_MODEL_DEPTH = 6


app = Flask(__name__,static_folder='static')
app.jinja_env.globals['include_raw'] = lambda filename : escape(app.jinja_loader.get_source(app.jinja_env, filename)[0])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/b2b', methods=['GET','POST'])
def b2b():
    if request.method == 'GET':
        return render_template('b2b.html', verificationresult = '')
    if request.method == 'POST':
        try:
            schema = xmlschema.XMLSchema('static/note.xsd')
        except:
            return render_template('b2b.html', verificationresult = 'Internal problem while loading XML schema. Please contact administration')

        result = "The file is not valid"
        
        try:
            file = request.files['file']
        except:
            file = None

        try:
            if file and file.filename.endswith('.xml'):
                if schema.is_valid(file.read().decode('utf-8')):
                    result = "The document is valid"
            else:
                file = None
        except:
            result = "Parse error"
            
        return render_template('b2b.html', verificationresult = result)

@app.route('/weakpassword')
def weakpassword():
    return render_template('weakpassword.html',searchresult = [], query = '')

@app.route('/weakpasswordsearch')
def weakpasswordsearch():
    conn = sqlite3.connect('passwords.db')
    result = []
    query = str(request.args.get('query'))
    
    if len(query) > 2:
        try:            
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM passwords WHERE ((password LIKE '%%%s' ) OR (password LIKE '%s%%')) LIMIT 20" % (query,query))            
            rows = cursor.fetchall()       
            for row in rows:
                print(row,file=sys.stderr)
                result.append(row[0])        
        except:
            result = []
    
    conn.close()
    return render_template('weakpassword.html',searchresult = result, query=query)

@app.route('/status')
def status():
    processes = json.loads(subprocess.check_output("/bin/ps aux | /usr/bin/awk -v OFS=, '{print $1, $2, $3}'|  /usr/bin/jq -R 'split(\",\") | {user: .[0], pid: .[1], cpu: .[2]}'| /usr/bin/jq -s .",shell=True))
    selection = []
    processes.pop(0)
    for proc in processes:
        if float(proc['cpu']) > 0:
            selection.append(proc)
    return render_template('status.html', processes = selection)

@app.route('/details', methods=['POST'])
def defauls():
    pid = str(request.form.get('pid'))
    try:
        processes = json.loads(subprocess.check_output("/bin/ps -p %s | /usr/bin/awk -v OFS=, '{print $1, $3, $4}'|  /usr/bin/jq -R 'split(\",\") | {pid: .[0], time: .[1], command: .[2]}'| /usr/bin/jq -s ." % (pid) ,shell=True))
        processes.pop(0)
        return render_template('details.html', processes = processes)
    except:
        processes = json.loads(subprocess.check_output("/bin/ps aux | /usr/bin/awk -v OFS=, '{print $1, $2, $3}'|  /usr/bin/jq -R 'split(\",\") | {user: .[0], pid: .[1], cpu: .[2]}'| /usr/bin/jq -s .",shell=True))
        selection = []
        processes.pop(0)
        for proc in processes:
            if float(proc['cpu']) > 0:
                selection.append(proc)
        return render_template('status.html', processes = selection)
    
if __name__ =='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port)



