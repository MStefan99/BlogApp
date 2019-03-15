from blog.utils.users import add_user, delete_user
from blog.utils.search import find_user_by_login, find_user_by_email, find_user_by_name
from blog.utils.check import check_login, check_email, check_username


def test_utils_login_exists():
    add_user('testUsername', 'testEmail@gmail.com', 'testPasswd', 'testCookie')

    assert check_login('testUsername')
    assert check_email('testEmail@gmail.com')


def test_utils_email_exists():
    add_user('testUsername', 'testEmail@gmail.com', 'testPasswd', 'testCookie')

    assert check_email('testEmail@gmail.com')


def test_utils_username_exists():
    add_user('testUsername', 'testEmail@gmail.com', 'testPasswd', 'testCookie')

    assert check_email('testEmail@gmail.com')


def test_utils_login_not_exists():
    user = find_user_by_login('testUserLogin')
    delete_user(user)

    assert not check_login('testUserLogin')


def test_utils_email_not_exists():
    user = find_user_by_email('testEmail@gmail.com')
    delete_user(user)

    assert not check_email('testEmail@gmail.com')


def test_utils_username_not_exists():
    user = find_user_by_name('testUsername')
    delete_user(user)

    assert not check_username('testUsername')

