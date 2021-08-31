from flask import Flask, render_template, redirect, url_for, request
# from data import data
import json
import time

from rich.theme import ThemeStack
from pegasus.pegasus import Pegasus

#  initialise flask
app = Flask(__name__)

# initialise data store
pegasus = Pegasus()


# Site API - html serving only


@app.route('/')
def home():

    return render_template('home.html', info=None)


@app.route('/command', methods=['GET', 'POST'])
def command():
    data = request.values['input']

    if data == '':
        return redirect('/')
    else:
        command_result = pegasus.run_command(data)
        return render_template('home.html', info=command_result)


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

    return(division_by_zero)


@app.errorhandler(404)
def page_not_found(e):

    return redirect(url_for('home', info=None))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
