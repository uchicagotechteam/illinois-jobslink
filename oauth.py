from oauth2client import client
from flask import Flask
from flask import *
from settings import *
import httplib2
import json
import sqlite3
from http import *

from apiclient.discovery import build
from apiclient.http import MediaFileUpload

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
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if 'credentials' not in session:
        return redirect(url_for('index'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())

    # Build Google Service for Fusion Table
    ft_service = build('fusiontables', 'v2', http_auth)

    # Query everything in database
    # for row in c.execute('SELECT * FROM listings'):
    #     format_row = tuple([e.encode() for e in row])
    #     print(format_row)
    #     ft_service.query().sql(
    #         sql="INSERT INTO " + FUSION_TABLE_ID + " (Name, 'Job Url') VALUES " +
    #         str(format_row) + ";").execute()
    media = MediaFileUpload(
        'listings.csv', mimetype='application/octet-stream', resumable=True)
    ft_service.table().importRows(tableId=FUSION_TABLE_ID,
                                  media_body=media, isStrict=False, encoding='auto-detect').execute()
    return "WE DID IT!!"


if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True)
