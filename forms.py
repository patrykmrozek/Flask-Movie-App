from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, RadioField, IntegerField, FloatField, BooleanField
from wtforms.validators import InputRequired, EqualTo


class RegistrationForm(FlaskForm):
    user_id = StringField('', validators=[InputRequired()])
    password = PasswordField('', validators=[InputRequired()])
    password2 = PasswordField('', validators=[InputRequired(), EqualTo("password")])
    profilepic = RadioField('', validators=[InputRequired()], choices=['pfp1.png',  'pfp2.png', 'pfp3.png', 'pfp4.png'], default="pfp1.png")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])
    submit = SubmitField("Submit")


class RateForm(FlaskForm):
    rating = SelectField("Rate Movie", choices=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
    review = StringField("Write A Review: ")
    favourite = BooleanField("Add To / Remove From Favourites", default=False)
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    search = StringField(validators=[InputRequired()])
    select = SelectField("Select", choices = ["users", "movies"])
    sort = RadioField("Sort By:", choices=['year', 'score'], default='year')
    submit=SubmitField('Submit')

class AdminMovieForm(FlaskForm):
    title = StringField()
    year = IntegerField()
    score = FloatField()
    director = StringField()
    poster = StringField(default="placeholder.png")
    description = StringField()
    submit = SubmitField()

class AddUserForm(FlaskForm):
    user_id = StringField("User: ", validators=[InputRequired()])
    password = StringField("Password: ", validators=[InputRequired()])
    admin = SelectField("Admin: ", choices=[0, 1], default=0)
    profilepic = SelectField("Profile Picture: ", choices=['pfp1.png',  'pfp2.png', 'pfp3.png', 'pfp4.png'], default="pfp1.png")
    submit = SubmitField("Submit")

class UpdateMovieForm(FlaskForm):
    title = StringField()
    year = IntegerField()
    score = FloatField()
    director = StringField()
    poster = StringField()
    description = StringField()
    submit = SubmitField()


class UpdateUserForm(FlaskForm):
    admin = SelectField(choices=[0, 1])
    submit = SubmitField()

