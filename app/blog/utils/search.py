from blog.globals import DATABASE


def find_user_by_name(username):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where lower(username) = lower(?)', [username])
    user = cursor.fetchone()
    return user


def find_user_by_email(email):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where lower(email) = lower(?) or '
                   'lower(verified_email) = lower(?)', [email, email])
    user = cursor.fetchone()
    return user


def find_user_by_cookie(cookie_id):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where cookieid = ?', [cookie_id])
    user = cursor.fetchone()
    return user


def find_user_by_login(login):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where lower(username) = lower(?) or '
                   'lower(email) = lower(?)', [login, login])
    user = cursor.fetchone()
    return user


def find_user_by_recover_key(key):
    cursor = DATABASE.cursor()
    cursor.execute('select * from users where recovery_link = ?', [key])
    user = cursor.fetchone()
    return user


def find_post_by_link(link):
    cursor = DATABASE.cursor()
    cursor.execute('select * from posts where link = ?', [link])
    return cursor.fetchone()


def find_post_by_id(id):
    cursor = DATABASE.cursor()
    cursor.execute('select * from posts where id = ?', [id])
    return cursor.fetchone()
