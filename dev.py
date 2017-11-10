import flask
from jinja2.utils import import_string
"""dev.py"""
dev = flask.Blueprint('dev', __name__, template_folder='templates')


@dev.route('/', methods={'GET'})
def index():
    """GET to generate a list of endpoints and their docstrings"""
    urls = dict([(r.rule, flask.current_app.view_functions[r.endpoint].__doc__)
                 for r in flask.current_app.url_map.iter_rules()
                 if not r.rule.startswith('/static')])

    vf = flask.current_app.view_functions.get('api.led')

    return flask.render_template('index.html', urls=urls)


@dev.route('/help', methods={'GET'})
def help():
    """Print all defined routes and their endpoint docstrings

    This also handles flask-router, which uses a centralized scheme
    to deal with routes, instead of defining them as a decorator
    on the target function.
    """
    routes = []
    for rule in flask.current_app.url_map.iter_rules():
        try:
            if rule.endpoint != 'static':
                if hasattr(flask.current_app.view_functions[rule.endpoint], 'import_name'):
                    import_name = flask.current_app.view_functions[rule.endpoint].import_name
                    obj = import_string(import_name)
                    routes.append({rule.rule: "%s\n%s" % (",".join(list(rule.methods)), obj.__doc__)})
                else:
                    routes.append({rule.rule: flask.current_app.view_functions[rule.endpoint].__doc__})
        except Exception as exc:
            routes.append({rule.rule:
                               "(%s) INVALID ROUTE DEFINITION!!!" % rule.endpoint})
            route_info = "%s => %s" % (rule.rule, rule.endpoint)
            flask.current_app.logger.error("Invalid route: %s" % route_info, exc_info=True)
            # func_list[rule.rule] = obj.__doc__

    return flask.jsonify(code=200, data=routes)
