import psycopg2

DATABASE = psycopg2.connect(user='flask', password='blogappflask', database='blog',
                            cursor_factory=psycopg2.extras.NamedTupleCursor)
DATABASE.autocommit = True


def exists(list):
    if list:
        return True
    else:
        return False


def find_user_by_name(username):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM users WHERE lower(username) = lower(%s)', (username,))
    user = cursor.fetchone()
    return user


def find_user_by_cookie(cookie_id):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM users WHERE cookieid = %s', (cookie_id,))
    user = cursor.fetchone()
    return user


def find_user_by_login(login):
    login = login.lower()
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM users WHERE lower(username) = lower(%s) or lower(email) = lower(%s)', (login, login))
    user = cursor.fetchone()
    return user


def find_user_by_recover_key(key):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM users WHERE recovery_link = %s', (key,))
    user = cursor.fetchone()
    return user


def check_username(username):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM users WHERE lower(username) = lower(%s)', (username,))
    user = cursor.fetchone()
    return exists(user)


def check_email(email):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM users WHERE lower(email) = lower(%s)', (email,))
    user = cursor.fetchone()
    return exists(user)


def find_post_by_link(link):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM posts WHERE link = %s', (link,))
    return cursor.fetchone()


def get_favourites(user):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM Posts JOIN Favourites '
                   'ON (Favourites.Post_ID = Posts.ID and Favourites.User_ID = %s) '
                   'ORDER BY Favourites.Date_Added DESC', (user.id,))
    return cursor.fetchall()


def find_post_by_id(id):
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = %s', (id,))
    return cursor.fetchone()
