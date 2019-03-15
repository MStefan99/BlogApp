from blog.utils.syntax_check import check_username_syntax, check_password_syntax, check_email_syntax


def test_username_ok():
    assert check_username_syntax('normal-username')


def test_username_too_short():
    assert not check_username_syntax('su')


def test_username_too_long():
    assert not check_username_syntax(
        '12345_here_goes_really_long_username_which_also_has_numbers_in_it_and_'
        'should_have_passed_the_test_if_it_was_not_so_long_that_it_even_does_not_fit_on_one_line')


def test_username_forbidden_symbols():
    assert not check_username_syntax('*?!":;№):ЖЭ/username123')


def test_email_ok():
    assert check_email_syntax('email@domain.com')
    assert check_email_syntax('i@domain.co')


def test_email_tld_too_short():
    assert not check_email_syntax('email@domain.c')


def test_email_no_tld():
    assert not check_email_syntax('email@domain')


def test_email_no_domain():
    assert not check_email_syntax('email@.com')


def test_email_no_domain_and_tld():
    assert not check_email_syntax('email@')


def test_email_no_at_sign():
    assert not check_email_syntax('email.domain.com')


def test_email_forbidden_symbols():
    assert not check_email_syntax('*?:;"*(@&^$#@.&%^')


def test_password_ok():
    assert check_password_syntax('password1111')


def test_password_no_numbers():
    assert not check_password_syntax('password')


def test_password_too_short():
    assert not check_password_syntax('passwd')
