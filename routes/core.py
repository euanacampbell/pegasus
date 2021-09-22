from pegasus.pegasus import Pegasus
from flask import Blueprint, render_template, request, redirect, url_for
core_routes = Blueprint('core_routes', __name__)

pegasus = Pegasus()


@core_routes.route('/')
def home():

    info = {}
    subcommands = [sub for sub in pegasus.sub_commands()]
    info['available_commands'] = pegasus.available_commands() + subcommands

    return render_template('home.html', info=info)


@core_routes.route('/<command>', methods=['GET', 'POST'])
def command(command):
    data = request.values['param']

    if command == '':
        return redirect(url_for('home'))

    command_result = pegasus.run_command(command + ' ' + data)
    command_result['command'] = command
    command_result['param'] = data
    return render_template('home.html', info=command_result)
