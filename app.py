import os
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.app_context().push()

if os.environ['FLASK_ENV'] == "testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_test'
    app.config['WTF_CSRF_ENABLED'] = False
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def show_all_pets():
    """ Displays all pets available for adoption. Will inform user if specific pet 
    has been adopted or not """

    pets = Pet.query.all()
    
    return render_template("base.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet(): 
    """ Handles GET and POST request for url. If form is not submitted or missing fields 
    when submitted, will display form to add new pet. If form is submitted, creates new pet and
    redirects user to home page. Pet defaults to available. """

    form = AddPetForm()

    if form.validate_on_submit(): 
        data = {k: v for k, v in form.data.items() if k != "csrf_token" and k != "photo_url"}
        photo_url = form.photo_url.data or None
        data["photo_url"] = photo_url

        new_pet = Pet(**data)

        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} has been added!")

        return redirect("/")

    else: 
        return render_template("pet_add_form.html", form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
def show_pet(pet_id):
    """ Handles GET and POST request for url. If form is not submitted, will display individual 
    page for pet selected along with a form to edit some information about the pet. If form is 
    submitted, edits pet information and redirects to individual pet page.  """

    pet = Pet.query.get_or_404(pet_id)

    form = EditPetForm(obj=pet)

    if form.validate_on_submit(): 
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        flash(f"{pet.name} has been updated!")
        
        return redirect(f"/{pet.id}")

    else: 
        return render_template("show_pet.html", form=form, pet=pet)

