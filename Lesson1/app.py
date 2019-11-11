from flask import Flask, render_template, request
import random
import time
import argon2

app = Flask(__name__)

pwhash = '\xcbR\xbb\xe6\xed\xf3f\xc1?\x10\x95\xf5<%e\xc3\xa6\xb1\xbd\x0f&\x82{<\x88\xa9\tq\xeea\xbc\xb5\xdf;\x90\xed\xd9\xc2Jf\xe6\x99\xcd\xc6\xbd\x15\x91\x92{R\xef\xfb\x93\xa9\xa0\xfa\x9f\xe0\xf8!\x86\x9f\x07\xe0E\xcf\xe4u\xc5]\x1e\x00y\x19Lv\xb0\xc94f\x7f\x13HM\x9bM\xca\xdf\xc3 \xcf+\x8a\xb1\xd6\x00\xcakd\xa98\x85\xd3\xc1f(\xea\xb9V\x1d\xb3\xee8"\x9dFEwT\xfb\xcc\x0c\xf7\xc2\xbd\xe5\x98y'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/guess', methods=['GET','POST'])
def guess():
    if request.method == 'GET':
        return render_template('guess.html', numtries = '0')

    time.sleep(2)
    
    
    r = random.randrange(1,20)
    number = request.form.get('number')
    if number == None:
        return render_template('guess.html',result = "Your input is ignored")
    else:
        number = int(number)
    if number in range(1,r):
        return render_template('guess.html',result = "the number is too low!")
    if number in range (r+1,20):
        return render_template('guess.html',result = "the number is too high!")
    else:
        return render_template('guess.html', result = "%d is correct!" % (number))

@app.route('/password', methods=['GET','POST'])
def password():
    if request.method == 'GET':
        return render_template('password.html')

    password = request.form.get('password')
    new = request.form.get('new')
    repeat = request.form.get('repeat')

    if ( password is not None and pwhash != argon2.argon2_hash(password=str(password), salt="XQEXFggkPcw9BtuGkn4ELm4a7r7MUKTjBW2fjaVv6ou8mJ9ZrfEQBYhiGqQ6LzRz", t=16, m=8, p=1, buflen=128, argon_type=argon2.Argon2Type.Argon2_i) ):
         return render_template('password.html', result = 'Password is not correct')
    if len(new) < 16:
        return render_template('password.html', result = 'Passwords length is too short (min 16 characters)')
    if ( new != repeat ):
        return render_template('password.html', result = 'New passwords are not the same')
    
    return render_template('password.html', result = 'Password changed succesfully!')

# file upload
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    f = request.files['file']

    if f.content_type != 'image/jpeg' and f.content_type != 'image/gif':
        return render_template('upload.html', result = "Only uploading of images is allowed")
        
    f.save('static/' + f.filename)
    return render_template('upload.html', result = 'File uploaded succesfully.')
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

