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
@app.route('/help')
def help():
    text = 'name, education, company, experience, job_type, temp_perm, hours'
    return 'Hey! Here is a list of available filters: %s' % (text)

# @app.route('/help') to list the available filters and
# @app.route('/') for a welcome page


@app.route('/jobs')
def get_jobs():
    c = get_db().cursor()

    # Build the query string
    query = 'SELECT * FROM listings'
    join_str = ' WHERE '

    # Get the parameters from the url
    name = request.args.get('name')
    education = request.args.get('education')
    company = request.args.get('company')
    experience = request.args.get('experience')
    job_type = request.args.get('job_type')
    perm = request.args.get('temp_perm')
    hours = request.args.get('hours')

    # Build the query string by appending values
    # city state industry company

    if name is not None:
        query += join_str + ('name = %s' % (name))
        join_str = ' AND '
    if education is not None:
        query += join_str + ('edu = %s' % (education))
        join_str = 'AND'
    if company is not None:
        query += join_str + ('company = %s' % (company))
        join_str = ' AND '
    if experience is not None:
        query += join_str + ('exp = %s' % (company))
        join_str = ' AND '
    if job_type is not None:
        query += join_str + ('employment = %s' % (company))
        join_str = ' AND '
    if perm is not None:
        query += join_str + ('temp = %s' % (company))
        join_str = ' AND '
    if hours is not None:
        query += join_str + ('hours = %s' % (company))

    print(query)
    results = []
    for row in c.execute(query):
        results.append(row)

    print(len(results))

    # Build a list with the tuples returned from sqlite and return a json
    return jsonify({'jobs': '\n'.join([', '.join(r) for r in results])})

if __name__ == "__main__":
    app.run(debug=True)
