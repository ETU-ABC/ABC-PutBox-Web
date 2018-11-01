from flask import Flask, render_template, request, json
import sqlite3 as sql

from flask_classful import FlaskView, route

app = Flask(__name__)

DATABASE = 'bil495-abc.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv



@app.route('/list')
def list():
    rows = query_db('select * from photo')
    return app.response_class(json.jsonify(rows), status=200)


@app.route('/albums', methods=["GET","PUT"])
def album():
    if request.method=="GET":
        rows = query_db('select * from album')
        return app.response_class(json.jsonify(rows), status=200)

    elif request.method =="PUT"
        query_db('INSERT INTO ALBUM (name, owner, first_photo)  VALUES(%s, %s, %s)')

if __name__ == '__main__':
    app.run(debug=False)
