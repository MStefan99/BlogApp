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
    current_password = request.form.get('current-password')
    database = sqlite3.connect('./database/db.sqlite')
    c = database.cursor()
    credentials = c.execute('SELECT * from Credentials').fetchall()

    if not username or not current_password:
        return render_template('error.html', code=1)

    for user_credentials in credentials:
        user_found = username.lower() == user_credentials[0].lower() or username == user_credentials[3]
        if user_found and pbkdf2_sha512.verify(current_password, user_credentials[1]):
            resp = make_response(render_template('success.html', code=0))
            resp.set_cookie('MSTID', user_credentials[2], max_age=60*60*24*30)
            return resp

    return render_template('error.html', code=2)


@app.route('/register_processor/', methods=['POST'])
def register_processor():
    username = request.form.get('username')
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')
    email = request.form.get('email')
    database = sqlite3.connect('./database/db.sqlite')
    c = database.cursor()
    credentials = c.execute('SELECT * from Credentials').fetchall()

    username_exists = username in [user_credentials[0] for user_credentials in credentials]
    email_exists = email in [user_credentials[3] for user_credentials in credentials]
    form_filled = username and new_password and repeat_new_password and email

    print(username)
    print(new_password)
    print(repeat_new_password)
    print(email)

    if not form_filled:
        return render_template('error.html', code=1)

    elif username_exists or email_exists:
        return render_template('error.html', code=0)

    elif new_password != repeat_new_password:
        return render_template('error.html', code=3)

    else:
        n = 255
        cookie_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))
        password_hash = pbkdf2_sha512.encrypt(new_password, rounds=200000, salt_size=64)
        c.execute('INSERT INTO Credentials (Username, Password, CookieID, Email) VALUES(?, ?, ?, ?)',
                  (username, password_hash, cookie_id, email))
        database.commit()
        resp = make_response(render_template('success.html', code=1))
        resp.set_cookie('MSTID', cookie_id, max_age=60*60*24*30)
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


@app.route('/settings/')
def settings():
    return render_template('settings.html')


@app.route('/settings_processor/', methods=['POST'])
def settings_processor():
    username = request.form.get('username')
    email = request.form.get('email')
    repeat_email = request.form.get('repeat-email')
    new_password = request.form.get('new-password')
    repeat_new_password = request.form.get('repeat-new-password')

    database = sqlite3.connect('./database/db.sqlite')
    c = database.cursor()
    credentials = c.execute('SELECT * from Credentials').fetchall()

    new_password_check = new_password == repeat_new_password
    email_check = email == repeat_email
    username_exists = username in [user_credentials[0] for user_credentials in credentials]

    for user_credentials in credentials:
        if request.cookies.get('MSTID') == user_credentials[2]:
            old_username = user_credentials[0]

    if not new_password_check:
        return render_template('error.html', code=3)
    elif not email_check:
        return render_template('error.html', code=4)
    elif username_exists:
        return render_template('error.html', code=0)

    if username:
        # noinspection PyUnboundLocalVariable
        c.execute('UPDATE Credentials SET Username = ? WHERE Username = ?', (username, old_username))
        database.commit()

    if email:
        c.execute('UPDATE Credentials SET Email = ? WHERE Username = ?', (email, old_username))
        database.commit()

    if new_password:
        password_hash = pbkdf2_sha512.encrypt(new_password, rounds=200000, salt_size=64)
        n = 255
        cookie_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))
        c.execute('UPDATE Credentials SET Password = ?, CookieID = ? WHERE Username = ?',
                  (password_hash, cookie_id, old_username))
        database.commit()
        resp = make_response(render_template('success.html', code=2))
        resp.set_cookie('MSTID', cookie_id, max_age=60*60*24*30)
        return resp

    return render_template('success.html', code=2)


@app.route('/delete/')
def delete():
    return render_template('delete.html')


@app.route('/delete_confirm/')
def delete_confirm():
    database = sqlite3.connect('./database/db.sqlite')
    c = database.cursor()
    credentials = c.execute('SELECT * from Credentials').fetchall()

    for user_credentials in credentials:
        if request.cookies.get('MSTID') == user_credentials[2]:
            username = user_credentials[0]

    # noinspection PyUnboundLocalVariable
    c.execute('DELETE FROM Credentials WHERE Username = ?', (username,))
    database.commit()
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run()
