from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
import os
import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bil495-abc.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


if __name__ == '__main__':
    app.run(debug=True)
    
