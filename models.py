"""Models for Adoption"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """ Connect to a database """
    db.app = app
    db.init_app(app)

class Pet(db.Model): 
    """ Models a pet available for adoption """

    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text, default="https://cdn2.vectorstock.com/i/1000x1000/88/26/no-image-available-icon-flat-vector-25898826.jpg")
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)
