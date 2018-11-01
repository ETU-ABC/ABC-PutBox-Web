from flask import Flask, render_template, request
import sqlite3 as sql

from json import dumps
from flask_classful import FlaskView, route

app = Flask(__name__)


class InternalView(FlaskView):
    def __init__(self):
        self.con = sql.connect("bil495-abc.db", check_same_thread=False)
        self.con.row_factory = sql.Row
        self.cur = self.con.cursor()

    @app.route('/add')
    def add(self):
        self.cur.execute(
            'INSERT INTO PHOTO (photo_path, upload_date, uploaded_by)  VALUES("afafddasf", "2018-03-30", 1)')
        rows = self.cur.fetchall();
        return app.response_class(str(rows), status=200)

    @app.route('/list')
    def list(self):
        self.cur.execute("select * from photo")

        rows = self.cur.fetchall();
        for row in rows:
            print(row)

        return app.response_class(str(rows), status=200)


InternalView.register(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
