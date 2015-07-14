from flask import Flask, request, render_template_string, jsonify, render_template, url_for
from models import db
from sites.manage import manage


app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
manage.load_site_handlers()


@app.route('/')
def index():
    welcome_text = """
    Welcome to account vip v1.0

    Now we support:
    {% for s in sites.keys() %}
        + {{ sites[s](action='get_info') }}
    {% endfor %}

    Support we for add account: {{ link_add_acc }}
    Extension for chrome: {{ link_ext_chrome }}

    And nothing more... :D
    """
    return render_template_string(
        welcome_text,
        sites=manage.sites,
        link_add_acc=url_for('add_account', _external=True),
        link_ext_chrome=url_for('static', filename='extension/account_vip.crx', _external=True)
    ), 200, {'Content-type': 'text/plain'}


@app.route('/login', methods=['POST'])
def login():
    site = request.args.get('site')
    data = request.get_json(force=True)
    if not site:
        return jsonify({'ok': False, 'error': 'Missing param site'}), 400, {}
    if 'cookies' not in data:
        return jsonify({'ok': False, 'error': 'Missing cookies data'}), 400, {}
    if site not in manage.sites.keys():
        return jsonify({'ok': False, 'error': 'Site temporary not support'}), 404, {}
    return manage.sites[site](action='login', data=data)


@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == "GET":
        return render_template('add_account.html', sites=manage.sites.keys())
    else:
        data = request.get_json(force=True)
        site = data.get('site', '')
        identity = data.get('identity', '')
        password = data.get('password', '')
        if site not in manage.sites.keys():
            return jsonify({'ok': False, 'error': 'Site temporary not support'}), 404, {}
        if not(identity and password):
            return jsonify({'ok': False, 'error': 'Missing identity or password'}), 400, {}
        return manage.sites[site](action='add_account', data=data)


@app.route('/get_script_clear_ads')
def get_script_clear_ads():
    site = request.args.get('site')
    if not site:
        return jsonify({'ok': False, 'error': 'Missing param site'}), 400, {}
    if site not in manage.sites.keys():
        return jsonify({'ok': False, 'error': 'Site temporary not support'}), 404, {}
    return manage.sites[site](action='get_script_clear_ads')

if __name__ == "__main__":
    app.run(debug=True)