from flask import Flask

app = Flask(__name__)


@app.errorhandler(500)
def api_internal_error(error):
    return 'INTERNAL ERROR', 500
