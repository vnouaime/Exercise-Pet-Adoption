from unittest import TestCase
from app import app
from flask import session, flash
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from wtforms.widgets import CheckboxInput
from wtforms import HiddenField

class FlaskTests(TestCase): 
    
    def setUp(self): 
        """Set up the Flask app for testing."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True 
        db.create_all()

    def tearDown(self): 
        """ Deletes test pets from database """ 

        db.session.close()

    ##############################################################################################################################
    def test_home_page(self):
        """ Tests home page to make sure that pets are displaying. Ensures that photo_url for pet is not blank """
        with app.test_client() as client:

            response = client.get("/")
            html = response.get_data(as_text=True)
            pets = Pet.query.all()

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="display-1 mb-5 text-center">Pets</h1>', html)
            self.assertIn('<h3 class="text-center mb-3 border-bottom">Available</h3>', html)
            self.assertIn('<h3 class="text-center mb-3 border-bottom">Not Available</h3>', html)
            self.assertIn('<a href="/add" class="btn btn-primary">Add Pet</a>', html)

            for pet in pets: 
                self.assertIn(f'<h5 class="card-title"><a href="/{pet.id}">{pet.name}</a></h5>', html)
                self.assertIsNotNone(pet.photo_url)
                
                if pet.available:
                    self.assertIn(f'<p class="card-text">{pet.name} is <b>available</b>!</p>', html)

                else: 
                    self.assertIn(f'<p class="card-text">{pet.name} is no longer available</p>', html)

    def test_add_pet_get(self):
        """ Tests GET request for adding new pet form route """
        with app.test_client() as client: 

            response = client.get("/add")
            html = response.get_data(as_text=True)
            
            form = AddPetForm()

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 class="display-2 text-center">Add New Pet</h1>', html)
            self.assertIn('<a href="/" class="btn btn-danger btn-lg">Go Back</a>', html)
            self.assertIn('<button class="btn btn-success btn-lg" type="submit">Submit</button>', html)
            
            for field in form: 
                if not isinstance(field, HiddenField):
                    self.assertIn(f'{field.label}', html)
                    self.assertIn(f'{field(class_="form-control")}', html)

    def test_add_pet_post(self):
        """ Tests POST request for adding new pet form route"""
        with app.test_client() as client: 
                
            data = {'name': 'Nova', 'species': 'porcupine', 'age': 5}

            response = client.post('/add', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            pet = Pet.query.filter_by(name="Nova").first()

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<h5 class="card-title"><a href="/{pet.id}">{pet.name}</a></h5>', html)
            self.assertIn(f'<div class="alert alert-success" role="alert">\n            Nova has been added!\n        </div>', html)
            self.assertIsNotNone(pet.photo_url)
            
            # Converts pet.name into bytes instead of string to check for flash message
            self.assertIn(f'{pet.name} has been added!'.encode(), response.data)

            ###########################################################################
            # Testing invalid request
            data = {'species': 'dog'}
            
            response_invalid = client.post('/add', data=data, follow_redirects=True)
            html_invalid = response_invalid.get_data(as_text=True)

            self.assertIn('<small class="form-text text-danger">\n                This field is required.\n              </small>\n            \n          </div>', html_invalid)

    def test_show_pet_get(self):
        """ Tests GET request for displaying individual pet page and edit form """
        with app.test_client() as client: 

            pet = Pet.query.get(5)
            response = client.get(f"/{pet.id}")
            html = response.get_data(as_text=True)
            
            form = EditPetForm(obj=pet)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<img src="{pet.photo_url}" class="card-img">', html)
            self.assertIn(f'<h4 class="card-title display-4 mb-2"><b>{pet.name}</b></h4>', html)
            self.assertIn(f'<p class="card-text" style="font-size: 20px;">Species: {pet.species}</p>', html)
            self.assertIn(f'<p class="card-text" style="font-size: 20px;">Age: {pet.age}</p>', html)
            self.assertIn(f'<h4 class="display-4 ml-4 mt-5">Edit {pet.name}</h4>', html)

            
            for field in form: 
                if not isinstance(field.widget, HiddenField):
                    if isinstance(field.widget, CheckboxInput):
                        self.assertIn(f'{field(class_="form-check-input")}', html)
                        self.assertIn(f'{field.label(class_="form-check-label")}', html)
                        
                else:  
                    self.assertIn(f'{field.label(class_="col-sm-2 col-form-label")}', html)
                    self.assertIn(f'{field(class_="form-control", placeholder="None Provided")}', html)
           
    def test_show_pet_post(self):
        """ Tests POST request for edit some fields for individual pet """
        with app.test_client() as client:

            pet = Pet.query.get(5)
            data = {'photo_url': 'https://brevardzoo.org/wp-content/uploads/2023/04/230503002-scaled.jpg', 'notes': 'Very cute!', 'available': None}

            response = client.post(f'/{pet.id}', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<img src="{pet.photo_url}" class="card-img">', html)
            self.assertIn(f'{pet.name} has been updated!'.encode(), response.data)

            ###########################################################################
            # Testing invalid request
            data = {'photo_url': 'dfhvlsdfhjlsdfjlsadefjsleflsef'}
            
            response_invalid = client.post(f'/{pet.id}', data=data, follow_redirects=True)
            html_invalid = response_invalid.get_data(as_text=True)

            self.assertIn('<small class="form-text text-danger">\n                    Invalid URL. Please enter a valid URL\n                    </small>\n                \n            </div>', html_invalid)
