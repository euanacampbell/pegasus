from flask import Blueprint, render_template, request, redirect, url_for
from pegasus.modules.sql import sql_config
from pegasus.modules.format import format

sql_routes = Blueprint('sql_routes', __name__)


@sql_routes.route('/sqlsetup')
def sql_default():

    return redirect(url_for('sql_routes.sql_setup', setting_type='queries'))


@sql_routes.route('/sqlsetup/<setting_type>')
def sql_setup(setting_type, alert=None):

    config = sql_config().load_config()

    for query in config['queries']:
        config['queries'][query]['query'] = format().format_sql(
            config['queries'][query]['query'])

    return render_template('sql_config.html', config=config, message=alert, setting_type=setting_type)


# QUERY
@sql_routes.route('/sql-api/newquery', methods=['GET', 'POST'])
def newquery():

    query_name = request.form.get('queryName', 0)

    sql_config().new_query(query_name, request.form.get(
        'connection', 0), request.form.get('query', 0))

    alert = {
        'type': 'success',
        'message': 'new query added'
    }

    return redirect(url_for('sql_routes.sql_setup', setting_type='queries', message=alert))


@sql_routes.route('/sql-api/updatequery', methods=['GET', 'POST'])
def updatequery():

    query_name = request.args.get("connName", 0)
    query = request.args.get('query', 0)
    connection = request.args.get('connection', 0)

    query = query.replace("\r", " ")
    query = query.replace("\n", " ")

    sql_config().new_query(query_name, connection, query)

    alert = {
        'type': 'success',
        'message': 'query updated'
    }

    return redirect(url_for('sql_routes.sql_setup', setting_type='queries', message=alert))


@sql_routes.route('/sql-api/deletequery/<query>', methods=['GET', 'POST'])
def deletequery(query):

    sql_config().delete_query(query)

    alert = {
        'type': 'success',
        'message': 'query deleted'
    }

    return redirect(url_for('sql_routes.sql_setup', setting_type='queries', message=alert))

# COMMAND


@sql_routes.route('/sql-api/deletecommand/<command>', methods=['GET', 'POST'])
def deletecommand(command):

    sql_config().delete_command(command)

    alert = {
        'type': 'success',
        'message': 'command deleted'
    }

    return redirect(url_for('sql_routes.sql_setup', setting_type='commands', message=alert))


@sql_routes.route('/sql-api/updatecommand', methods=['GET', 'POST'])
def updatecommand():

    enabled_queries = [i for i in request.values]
    command_name = request.form.get('commandName', 0)

    sql_config().update_command(command_name, enabled_queries)

    alert = {
        'type': 'success',
        'message': 'command updated'
    }

    return redirect(url_for('sql_routes.sql_setup', setting_type='commands', message=alert))

# SETTINGS


@sql_routes.route('/sql-api/updatesettings', methods=['GET', 'POST'])
def updatesettings():

    enabled_settings = [i for i in request.values]

    print(enabled_settings)

    sql_config().update_settings(enabled_settings)

    alert = {
        'type': 'success',
        'message': 'settings updated'
    }

    return redirect(url_for('sql_routes.sql_setup', setting_type='settings', message=alert))

# CONNECTION


@sql_routes.route('/sql-api/deleteconn/<conn>', methods=['GET', 'POST'])
def deleteconn(conn):

    sql_config().delete_conn(conn)

    return redirect(url_for('sql_routes.sql_setup'))


@sql_routes.route('/sql-api/updateconn', methods=['GET', 'POST'])
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

    return redirect(url_for('sql_routes.sql_setup'))
