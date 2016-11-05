from oauth2client import client
from flask import Flask
from flask import *
from settings import *
import httplib2
import json

from apiclient.discovery import build

app = Flask(__name__)


@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())

    ft_service = build('fusiontables', 'v2', http_auth)
    tables = ft_service.table().list().execute()
    return json.dumps(tables)


@app.route('/callback')
def callback():
    flow = client.flow_from_clientsecrets(
        'client_secret_911503641744-hn8pinmojgfi1n4poh2n8ssk48bu8idn.apps.googleusercontent.com.json',
        scope='https://www.googleapis.com/auth/fusiontables',
        redirect_uri='http://localhost:5000/callback')

    flow.params['access_type'] = 'offline'

    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        return redirect(url_for('index'))


@app.route('/update')
def update():
    if 'credentials' not in session:
        return redirect(url_for('index'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())

    ft_service = build('fusiontables', 'v2', http_auth)
    ft_service.query().sql(
        sql="INSERT INTO 1WOu6DaHenRNNXIWHkNWjGf66sUCnfl5fLQHhHOwt (col0) VALUES ('TODO');").execute()

    ft_service.column().insert(tableId='1WOu6DaHenRNNXIWHkNWjGf66sUCnfl5fLQHhHOwt',
                               body=dict(kind="fusiontables#column", columnId=307, type="String", name="my_col"))
    return "WE DID IT!!"


if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True)
