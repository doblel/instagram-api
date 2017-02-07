"""Flask example."""
from flask import Flask, redirect, request, session, url_for, jsonify
from instagram import Instagram

CONFIG = {
    'client_id': '<client_id>',
    'client_secret': '<client_secret>',
    'redirect_uri': '<redirect_uri>'
}

app = Flask(__name__)
app.secret_key = 'secret'

instagram_api = Instagram(**CONFIG)


@app.route('/')
def index():
    user = session.get('user', None)

    if user is not None:
        api = Instagram()
        data = api.self(access_token=user['access_token'])
        return jsonify(data)

    return 'No user'


@app.route('/login')
def login():
    url = instagram_api.auth_url()
    return redirect(url)


@app.route('/user/oauh')
def oaut_callback():
    code = request.args.get('code', None)

    if code is None:
        return 'no code'

    try:
        user_info = instagram_api.exchange_code_for_token(code)

        session['user'] = user_info

        return redirect(url_for('index'))

    except Exception as e:
        print 'except %s' % str(e)


if __name__ == '__main__':
    app.run(debug=True)
