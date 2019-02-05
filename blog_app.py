from flask import Flask, render_template, request, make_response, redirect
from passlib.hash import pbkdf2_sha512
import random
import string
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    if request.cookies.get('MSTID'):
        database = sqlite3.connect('./database/db.sqlite')
        c = database.cursor()
        credentials = c.execute('SELECT * from Credentials').fetchall()
        for user_credentials in credentials:
            if request.cookies.get('MSTID') == user_credentials[2]:
                return redirect('/account/', code=302)
    return render_template('select.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/login_processor/', methods=['POST'])
def login_processor():
    username = request.form.get('login')
    passwd = request.form.get('password')
    database = sqlite3.connect('./database/db.sqlite')
    c = database.cursor()
    credentials = c.execute('SELECT * from Credentials').fetchall()

    if not username or not passwd:
        return render_template('error.html', code=1)

    for user_credentials in credentials:
        user_found = username == user_credentials[0] or username == user_credentials[3]
        if user_found and pbkdf2_sha512.verify(passwd, user_credentials[1]):
            resp = make_response(render_template('success.html', code=0))
            resp.set_cookie('MSTID', user_credentials[2], max_age=60*60*24)
            return resp

    return render_template('error.html', code=2)


@app.route('/register_processor/', methods=['POST'])
def register_processor():
    username = request.form.get('login')
    passwd = request.form.get('password0')
    passwd_repeat = request.form.get('password1')
    email = request.form.get('email')
    database = sqlite3.connect('./database/db.sqlite')
    c = database.cursor()
    credentials = c.execute('SELECT * from Credentials').fetchall()

    username_exists = username in [user_credentials[0] for user_credentials in credentials]
    email_exists = email in [user_credentials[3] for user_credentials in credentials]
    form_filled = username and passwd and passwd_repeat and email

    if not form_filled:
        return render_template('error.html', code=1)

    elif username_exists or email_exists:
        return render_template('error.html', code=0)

    elif passwd != passwd_repeat:
        return render_template('error.html', code=3)

    else:
        n = 255
        cookie_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))
        password_hash = pbkdf2_sha512.encrypt(passwd, rounds=200000, salt_size=16)
        c.execute('''INSERT INTO Credentials (Login, Password, CookieID, Email) VALUES(?, ?, ?, ?)''',
                  (username, password_hash, cookie_id, email))
        database.commit()
        resp = make_response(render_template('success.html', code=1))
        resp.set_cookie('MSTID', cookie_id, max_age=60*60*24)
        return resp


@app.route('/logout/')
def logout():
    resp = make_response(redirect('/', code=302))
    resp.set_cookie('MSTID', 'Bye!', expires=0)
    return resp


@app.route('/account/')
def account():
    database = sqlite3.connect('./database/db.sqlite')
    c = database.cursor()
    credentials = c.execute('SELECT * from Credentials').fetchall()
    for user_credentials in credentials:
        if request.cookies.get('MSTID') == user_credentials[2]:
            return render_template('account.html', username=user_credentials[0])
    return redirect('/logout/', code=302)


if __name__ == '__main__':
    app.run()
