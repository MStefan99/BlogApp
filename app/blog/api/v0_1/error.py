from flask import Blueprint

api_v01_error = Blueprint('api v0_1 error', __name__)


@api_v01_error.errorhandler(500)
def api_internal_error(error):
    return 'INTERNAL ERROR', 500
