""" Seed file to make sample data for dbs """
import os
from models import db, connect_db, Pet
from app import app

if os.environ['FLASK_ENV'] == "testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_test'
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption'

db.drop_all()
db.create_all()

Pet.query.delete()

new_pet_1 = Pet(name="Leo", species="dog", photo_url="https://www.hepper.com/wp-content/uploads/2022/08/Black-Labrador-Retrievers.jpg", age=4, notes="Friendly!", available=False)
new_pet_2 = Pet(name="Ophelia", species="dog", photo_url="https://images.squarespace-cdn.com/content/v1/54e7a1a6e4b08db9da801ded/1bd563c1-7bbb-4b44-af21-a60408b6f129/44.png", age=1)
new_pet_3 = Pet(name="Frankie", species="cat", photo_url="https://guidedpet.com/wp-content/uploads/2023/08/Kitten-Not-Grooming-Himself.jpg", age=2, available=False)
new_pet_4 = Pet(name="Spike", species="porcupine", photo_url="https://guidedpet.com/wp-content/uploads/2023/08/Kitten-Not-Grooming-Himself.jpg", age=6)
new_pet_5 = Pet(name="Bean", species="cat")

db.session.add_all([new_pet_1, new_pet_2, new_pet_3, new_pet_4, new_pet_5])
db.session.commit()