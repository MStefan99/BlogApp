from flask import Flask, render_template, request, make_response
import random
import string
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('select.html')


@app.route('/login/')
def login():
    if request.cookies.get("MSTID"):
        database = sqlite3.connect("credentials.sqlite")
        c = database.cursor()
        credentials = c.execute('SELECT * from Credentials').fetchall()
        for user_credentials in credentials:
            if request.cookies.get("MSTID") == user_credentials[2]:
                return render_template('success.html', code=2, username=user_credentials[0])

    return render_template('login.html')


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/login_processor', methods=["POST"])
def login_processor():
    username = request.form.get("login")
    password = request.form.get("password")
    database = sqlite3.connect("credentials.sqlite")
    c = database.cursor()
    credentials = c.execute('SELECT * from Credentials').fetchall()

    for user_credentials in credentials:
        if username == user_credentials[0] and password == user_credentials[1]:
            resp = make_response(render_template('success.html', code=0))
            resp.set_cookie("MSTID", user_credentials[2], max_age=60*60*24)
            return resp

    return render_template('error.html', code=2)


@app.route("/register_processor", methods=["POST"])
def register_processor():
    username = request.form.get("login")
    password0 = request.form.get("password0")
    password1 = request.form.get("password1")
    database = sqlite3.connect("credentials.sqlite")
    c = database.cursor()

    credentials = c.execute('SELECT Login from Credentials').fetchall()
    if not username or not password0 or not password1:
        return render_template('error.html', code=1)

    elif username in [user_credentials[0] for user_credentials in credentials]:
        return render_template('error.html', code=0)

    elif password0 != password1:
        return render_template('error.html', code=3)

    else:
        n = 30
        cookie_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))
        c.execute('''INSERT INTO Credentials (Login, Password, CookieID) VALUES(?, ?, ?)''', (username, password0, cookie_id))
        database.commit()
        resp = make_response(render_template("success.html", code=1))
        resp.set_cookie('MSTID', cookie_id, max_age=60*60*24)
        return resp


@app.route('/logout')
def logout():
    resp = make_response(render_template('select.html'))
    resp.set_cookie("MSTID", "Bye!", expires=0)
    return resp


if __name__ == '__main__':
    app.run()
