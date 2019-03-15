import re


def must_contain(characters, number=1):
    return f'(?=.*[{characters}]{{{number},}})'


def length(minimum, maximum=100):
    return f'{{{minimum},{maximum}}}'


numbers = '0-9'
letters = 'a-zA-Z'
password_allowed_symbols = f'[{numbers}{letters}!@#$%^&*(){{}}\\[\\]\\-_=+,.<>|\\\\]'
username_allowed_symbols = f'[{numbers}{letters}\\-_.]'
password_re = f'^{must_contain(letters)}{must_contain(numbers)}{password_allowed_symbols}{length(8)}$'
username_re = f'^{must_contain(letters)}{username_allowed_symbols}{length(3)}$'
email_re = '^(([^<>()\\[\\]\\\\.,;:\\s@"][\\w]*(\\.[^<>()\\[\\]\\\\.,;:\\s@"][\\w]+)*)|("\\w+"))@((\\[[0-9]{1,' \
           '3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$'


def check_password_syntax(password):
    return True if password and re.search(password_re, password) else False


def check_username_syntax(username):
    return True if username and re.search(username_re, username) else False


def check_email_syntax(email):
    return True if email and re.search(email_re, email) else False
