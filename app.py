from flask import Flask, render_template, request, json, g
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


@app.route('/albums', methods=["GET","PUT"])
def album():

    if request.method=="GET":
        cur = get_db().execute('select * from album')
        data = cur.fetchall()
        print(data)
        return app.response_class(json.dumps(data), status=200)

    elif request.method =="PUT":
        data = request.json
        get_db().execute("INSERT INTO ALBUM(name, owner, first_photo) VALUES(?,?,?)",(data["name"], data["owner"], data["first_photo"]))
        get_db().commit()
        return app.response_class("Inserted\n", status=200)


@app.route('/photos/<photo_id>', methods=['GET', 'PUT'])
def retrieve_photos(photo_id):

    if request.method == 'GET':
        data = query_db('SELECT * FROM photo WHERE photo_id = ?', [photo_id])
        return app.response_class(json.dumps(data), status=200)

    elif request.method =='PUT':
        #data = request.json
        #get_db().execute("INSERT INTO PHOTO(name, owner, first_photo) VALUES(?,?,?)",(data["photo_path"], data["upload_date"], data["first_photo"]))
        #get_db().commit()
        return app.response_class("Inserted\n", status=200)


if __name__ == '__main__':
    app.run(debug=False)
