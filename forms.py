from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class AddPetForm(FlaskForm): 
    """ Form for adding new pet """

    name = StringField("Pet Name", 
                       validators=[InputRequired()])
    species = SelectField("Species", 
                         choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')],
                         validators=[InputRequired()])
    photo_url = StringField("Photo URL",
                           validators=[
                            Optional(), 
                            URL(message="Invalid URL. Please enter a valid URL")])
    age = IntegerField("Age", 
                      validators=[
                        Optional(),
                        NumberRange(min=0, max=30, message="Age must be between 0 and 30")])
    notes = TextAreaField("Notes", 
                         validators=[Optional()])

    
class EditPetForm(FlaskForm): 
    """ Form for editing some pet information """

    photo_url = StringField("Photo URL",
                           validators=[
                            Optional(), 
                            URL(message="Invalid URL. Please enter a valid URL")])

    notes = TextAreaField("Notes", 
                        validators=[Optional()])

    available = BooleanField("Check if Available")



