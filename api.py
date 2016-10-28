from flask import Flask
from flask import *
from settings import *
import sqlite3

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# query string is of the following format
# 'http://localhost:5000/jobs?name=<STRING>&id=<STRING>&...'
# name = <string>
# id = <string>
# other parameters = (date posted?, zipcode?, education?, etc.)


@app.route('/jobs')
def get_jobs():
    c = get_db().cursor()

    # Build the query string
    query = 'SELECT * FROM listings'
    join_str = ' WHERE '

    # Get the parameters from the url
    name = request.args.get('name')
    id_num = request.args.get('id')
    date = request.args.get('date')
    zip = request.args.get('zip')
    education = request.args.get('education')


# city, state, industry, company, date, zip, education, wage, 
    # Build the query string by appending values
    if name is not None:
        query += join_str + ('name = %s' % (name))
        join_str = ' AND '
    if name is not None:
        query += join_str + ('id = %s' % (id_num))
        join_str = ' AND '
    if date is not None:
        query += join_str + ('date = %s' % (date))
        join_str = 'AND'
    if zip is not None:
        query += join_str + ('zip = %s' % (zip))
        join_str = 'AND'
    if education is not None:
        query += join_str + ('education = %s' % (education))
        join_str = 'AND'
 #   if wage 


    for row in c.execute(query):
        print row

    # Build a list with the tuples returned from sqlite and return a json
    return jsonify({'jobs': '\n'.join([', '.join(r) for r in c])})

if __name__ == "__main__":
    app.run(debug=True)
