from flask import Flask, render_template, redirect, url_for, request
from routes.sql_routes import sql_routes
from routes.core import core_routes
from routes.error_handling import error_routes

from pegasus.pegasus import Pegasus


#  initialise flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.register_blueprint(sql_routes)
app.register_blueprint(core_routes)
app.register_blueprint(error_routes)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
