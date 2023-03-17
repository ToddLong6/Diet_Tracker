from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DecimalField, RadioField, DateField, SelectField, \
    IntegerField, EmailField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email, URL, Length, NumberRange
from flask_ckeditor import CKEditorField
from datetime import datetime


def time():
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    return today_date

def yesterday():
    pass

date = time()


class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    email = EmailField("Enter Email", validators=[DataRequired()])
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match'),
                                              Length(min=6, max=14,
                                                     message='Field must be between 6 and 14 characters long.')])
    confirm = PasswordField('Repeat Password')
    s_weight = DecimalField("Weight ", validators=[DataRequired(), NumberRange(min=None, max=500, message=None)],
                          places=1, description='(Enter in lbs)', render_kw={"placeholder": "Enter your weight"})
    height = IntegerField("Height", validators=[DataRequired(), NumberRange(min=None, max=100, message=None)],
                          description='(Enter in inches)', render_kw={"placeholder": "Enter your height"})
    gender = SelectField("Gender", choices=["Male", "Female"], coerce=str,option_widget=None, validate_choice=True)
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=None, max=100, message=None)])
    register = SubmitField('Register')


class Sign_in(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', [InputRequired()])
    login = SubmitField('Login')


class WeightForm(FlaskForm):
    weight = DecimalField(" ", validators=[DataRequired(), NumberRange(min=None, max=1000, message=None)], places=1,
                          description='(Enter in lbs)', render_kw={"placeholder": "Enter your weight"})
    date = DateField(' ', format='%Y-%m-%d', render_kw={"placeholder": date})
    submit = SubmitField('Submit')


class FoodForm(FlaskForm):
    food = StringField("Enter Food", validators=[DataRequired()], render_kw={"placeholder": "I eat 3 cups of beans"})
    date = DateField(' ', format='%Y-%m-%d', render_kw={"placeholder": date})
    meal = SelectField("Type of Meal", choices=["Breakfast", "Lunch", "Dinner", "Snack"], coerce=str,
                       option_widget=None, validate_choice=True)
    submit = SubmitField('Submit')


class ExerciseForm(FlaskForm):
    exercise = StringField("Enter Workout ", validators=[DataRequired()],
                           render_kw={"placeholder": "I walk 3 mile and did 50 push up"})
    date = DateField(' ', format='%Y-%m-%d', render_kw={"placeholder": date})
    submit = SubmitField('Submit')

class DateForm(FlaskForm):
    date = DateField(' ', format='%Y-%m-%d', render_kw={"placeholder": date})
    submit1 = SubmitField('Submit')