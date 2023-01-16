from flask import Blueprint, render_template

web_error = Blueprint('web-error', __name__)


@web_error.route('/check_email/', methods=['GET'])
@web_error.route('/check_username/', methods=['GET'])
@web_error.route('/add_post/', methods=['GET'])
@web_error.route('/del-post/', methods=['GET'])
@web_error.route('/register_processor/', methods=['GET'])
@web_error.route('/login_processor/', methods=['GET'])
@web_error.route('/smart sign in/', methods=['GET'])
@web_error.route('/settings_processor/', methods=['GET'])
def web_wrong_route():
    return render_template('status/error.html', code='wrong_route')


@web_error.errorhandler(404)
def web_page_not_found(error):
    title = 'Page not found!'
    message = 'Oops! It\'s not you, it\'s us! Seems like we\'ve lost this page somewhere in space...'
    return render_template('status/app_error.html', code=404, title=title, message=message, error=error), 404


@web_error.errorhandler(500)
def web_internal_error(error):
    title = 'Server error!'
    message = 'Oops! It\'s not you, it\'s us! Seems like our programmers messed up this page...'
    return render_template('status/app_error.html', code=500, title=title, message=message, error=error), 500
