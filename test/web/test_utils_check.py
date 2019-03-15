from blog.utils.users import delete_user
from blog.utils.search import find_user_by_login
from blog.utils.check import check_login


def test_web_login_exists():
    user = find_user_by_login('testUser')
    try:
        delete_user(user)
    except TypeError as e:
        print(e)
    assert not check_login('testUser')
