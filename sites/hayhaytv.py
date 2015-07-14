import requests
from flask import jsonify, url_for
from sqlalchemy.sql.expression import func
from models import db, Account
from .manage import manage

login_url = 'http://www.hayhaytv.vn/ajax_jsonp.php?p=jsonp_login'
session_key = 'PHPSESSID'


@manage.add_site('www.hayhaytv.vn')
def handle_hayhay(**kwargs):
    description = 'Hayhaytv'
    action = kwargs.get('action', '')
    data = kwargs.get('data', {})

    if action == 'add_account':
        form_data = {
            'email': data['identity'],
            'password': data['password']
        }
        resp = requests.post(login_url, data=form_data)
        resp_data = resp.json()
        if resp_data['object'] == "check_login" and resp_data.get('success', '') == 'success':
            acc = Account()
            acc.site = 'www.hayhaytv.vn'
            acc.identity = data['identity']
            acc.password = data['password']
            db.session.add(acc)
            db.session.commit()
            return jsonify({'ok': True})
        return jsonify({'ok': False})
    elif action == 'login':
        acc = Account.query.filter(Account.site == 'www.hayhaytv.vn').order_by(func.random()).limit(1)
        if acc.all():
            acc = acc.all()[0]
        else:
            return jsonify({'ok': False, 'error': 'No have account'})
        form_data = {
            'email': acc.identity,
            'password': acc.password
        }
        requests.post(login_url, data=form_data, cookies={session_key: str(data['cookies'][session_key])})
        return jsonify({'ok': True})
    elif action == 'get_script_clear_ads':
        return jsonify({
            'ok': True,
            'data': {'url': url_for('static', filename='js/hayhaytv_clear_ads.js', _external=True)}
        })
    elif action == 'get_info':
        return description + ': Login vip, clear ads'