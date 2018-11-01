from flask import Flask, render_template, request, g
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


class InternalView(FlaskView):
    @app.route('/add')
    def add(self):
        rows = query_db('INSERT INTO PHOTO (photo_path, upload_date, uploaded_by)  VALUES("afafddasf", "2018-03-30", 1)')

        return app.response_class(str(rows), status=200)

    @app.route('/list')
    def list(self):
        rows = query_db('select * from photo')
        print(rows)

        return app.response_class(str(rows), status=200)


InternalView.register(app)
if __name__ == '__main__':
    app.run(debug=False)
