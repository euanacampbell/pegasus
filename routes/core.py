from platform import version
from pegasus.pegasus import Pegasus
from pegasus.modules.update import update
from flask import Blueprint, render_template, request, redirect, url_for
core_routes = Blueprint('core_routes', __name__)


pegasus = Pegasus()

current_version = update().__VERSION__


@core_routes.route('/')
def home():

    return render_template('home.html', info=None, version=current_version)


@core_routes.route('/<command>', methods=['GET', 'POST'])
def command(command):
    try:
        data = request.values['param']
    except:
        data = ''

    if command == '':
        return redirect(url_for('home'))

    command_result = pegasus.run_command(command + ' ' + data)
    command_result['command'] = command
    command_result['param'] = data
    return render_template('home.html', info=command_result, version=current_version)
