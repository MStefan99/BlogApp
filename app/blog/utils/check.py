from blog.utils.search import find_user_by_name, find_user_by_login, find_user_by_email


def exists(list):
    if list:
        return True
    else:
        return False


def check_username(username):
    user = find_user_by_name(username)
    return exists(user)


def check_login(login):
    user = find_user_by_login(login)
    return exists(user)


def check_email(email):
    user = find_user_by_email(email)
    return exists(user)
