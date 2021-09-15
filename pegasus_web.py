from flask import Flask, render_template, redirect, url_for, request

from pegasus.pegasus import Pegasus
from pegasus.modules.sql import sql_config

#  initialise flask
app = Flask(__name__)

# initialise data store
pegasus = Pegasus()


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


@app.route('/sqlsetup')
def sql_setup():

    return render_template('sql_configuration.html', config=sql_config().load_config(), message=None)


@app.route('/sqlsetup/updatecombi/<combicommand>', methods=['GET', 'POST'])
def updatecombi(combicommand):

    enabled_commands = [i for i in request.values]

    sql_i = sql_config()
    sql_i.update_combi(combicommand, enabled_commands)

    return redirect(url_for('sql_setup'))


@app.route('/sqlsetup/deletequery/<query>', methods=['GET', 'POST'])
def deletequery(query):

    sql_config().delete_query(query)

    return redirect(url_for('sql_setup'))


@app.route('/sqlsetup/deletecommand/<command>', methods=['GET', 'POST'])
def deletecommand(command):

    sql_config().delete_command(command)

    return redirect(url_for('sql_setup'))


@app.route('/sqlsetup/newquery', methods=['GET', 'POST'])
def newquery():

    enabled_commands = [i for i in request.values if i != 'combiName']
    query_name = request.form.get('queryName', 0)

    sql_config().new_query(query_name, request.form.get(
        'connection', 0), request.form.get('query', 0))

    return redirect(url_for('sql_setup'))


@app.route('/sqlsetup/updatesettings', methods=['GET', 'POST'])
def updatesettings():

    enabled_settings = [i for i in request.values]

    print(enabled_settings)

    sql_config().update_settings(enabled_settings)

    return redirect(url_for('sql_setup'))


@app.route('/sqlsetup/deleteconn/<conn>', methods=['GET', 'POST'])
def deleteconn(conn):

    sql_config().delete_conn(conn)

    return redirect(url_for('sql_setup'))


@app.route('/sqlsetup/updateconn', methods=['GET', 'POST'])
def updateconn():
    conn_name = request.form.get('connName', 0)

    conn_setup = {
        'type': request.form.get('type', 0),
        'type': request.form.get('type', 0),
        'server': request.form.get('server', 0),
        'database': request.form.get('database', 0),
        'username': request.form.get('username', 0),
        'password': request.form.get('password', 0)
    }

    sql_config().update_conn(conn_name, conn_setup)

    return redirect(url_for('sql_setup'))


@app.route('/sqlsetup/updatecommand', methods=['GET', 'POST'])
def updatecommand():
    command_name = request.form.get('commandName', 0)

    enabled_queries = [i for i in request.values]

    enabled_queries.remove('commandName')

    sql_config().update_command(command_name, enabled_queries)

    return redirect(url_for('sql_setup'))


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

    return(division_by_zero)


# @app.errorhandler(404)
# def page_not_found(e):

#     return redirect(url_for('home', info=None))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
