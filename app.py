from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
from nutritionix import get_food, get_exercise
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import WeightForm, FoodForm, ExerciseForm, RegisterForm, Sign_in, time, DateForm
import pandas as pd
# from dotenv import load_dotenv
import os

app = Flask(__name__)

# load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = SECRET_KEY
# Flask-Bootstrap requires this line
Bootstrap(app)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Functions
def get_weight():
    db_weight = Weight.query.filter_by(users_id=current_user.id).order_by(asc(Weight.date)).all()
    last_weights = []
    for i in db_weight:
        last_weights.append(i.weight)
    if not last_weights:
        display_weight = 1
    else:
        display_weight = last_weights[-1]
    return display_weight


def get_weight_loss():
    starting_weight = current_user.s_weight
    current_weight = get_weight()
    weight_loss = starting_weight - current_weight
    return weight_loss


def get_all_weight_dates(table):
    db_weight = table.query.filter_by(users_id=current_user.id).order_by(asc(table.date)).all()
    date_weights = []
    for i in db_weight:
        date_weights.append(i.date)
    return date_weights


def get_all_weight():
    db_weight = Weight.query.filter_by(users_id=current_user.id).order_by(asc(Weight.date)).all()
    all_weights = []
    for i in db_weight:
        all_weights.append(i.weight)
    return all_weights


def get_all_total_calories():
    db_intake = Intake.query.filter_by(users_id=current_user.id).order_by(asc(Intake.date)).all()
    all_calories = []
    for i in db_intake:
        all_calories.append(i.total_calories)
    return all_calories


def get_all_total_sugar():
    db_intake = Intake.query.filter_by(users_id=current_user.id).order_by(asc(Intake.date)).all()
    all_sugar = []
    for i in db_intake:
        all_sugar.append(i.total_sugar)
    return all_sugar

def get_calories():
    intake_form = DateForm()
    db_food = Food.query.filter_by(food_id=current_user.id, date=intake_form.date.data).all()
    all_cal = [cal.calories for cal in db_food]
    all_sugar = [cal.sugar for cal in db_food]
    intake_food = Intake(
        date=intake_form.date.data,
        total_sugar=int(sum(all_sugar)),
        total_calories=int(sum(all_cal)),
        users_id=current_user.id
    )
    # user_exist = Intake.query.filter_by(users_id=current_user.id).all()
    # date_exist = Intake.query.filter_by(date=intake_form.date.data).all()
    with app.app_context():
        db.session.add(intake_food)
        db.session.commit()
        return "Was added"


def count_exercise():
    db_exercise = Exercise.query.filter_by(exercise_id=current_user.id).all()
    all_exercises = [item.item for item in db_exercise]
    count = pd.Series(all_exercises).value_counts()
    exercise_dict = {}
    for name, num in count.items():
        exercise_dict[name] = num
    return exercise_dict


def burned_calories():
    burns_form = DateForm()
    db_exercise = Exercise.query.filter_by(exercise_id=current_user.id, date=burns_form.date.data).all()
    all_cal = [cal.calories for cal in db_exercise]
    burned_food = Losses(
        date=burns_form.date.data,
        total_calories_loss=int(sum(all_cal)),
        users_id=current_user.id
    )
    with app.app_context():
        db.session.add(burned_food)
        db.session.commit()
        return "Was added"

def total_calories():
    db_burns = Losses.query.filter_by(users_id=current_user.id).order_by(asc(Losses.date)).all()
    burned_calorie = []
    for cal in db_burns:
        burned_calorie.append(cal.total_calories_loss)
    return burned_calorie

# Variables
time = time()

# Table for Database
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    s_weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    # User Can have many Weight
    weights = db.relationship("Weight", backref="users")

class Weight(db.Model):
    __tablename__ = "weight"
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(250), nullable=False)
    # Foreign Key to Link User
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Food(db.Model):
    __tablename__ = "food"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    sugar = db.Column(db.Integer, nullable=False, default=0)
    calories = db.Column(db.Integer, nullable=False, default=0)
    meal = db.Column(db.String(250), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Exercise(db.Model):
    __tablename__ = "exercise"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class Intake(db.Model):
    __tablename__ = "intake"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(250), nullable=False)
    total_calories = db.Column(db.Integer, nullable=False, default=0)
    total_sugar = db.Column(db.Integer, nullable=False, default=0)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class Losses(db.Model):
    __tablename__ = "loss"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(250), nullable=False)
    total_calories_loss = db.Column(db.Integer, nullable=False, default=0)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

with app.app_context():
    #db.drop_all()
    db.create_all()


# App components
@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect("login")
    else:
        db_weight = Weight.query.all()
        display_weight = get_weight()
        date_list = get_all_weight_dates(Weight)
        weight_list = get_all_weight()
        weight_percent = int((get_weight_loss() / display_weight) * 100)
        all_calories = get_all_total_calories()
        all_dates = get_all_weight_dates(Intake)
        burned_calorie = total_calories()

        return render_template("index.html", db_weight=db_weight, display_weight=display_weight,
                               current_user=current_user, date_list=date_list, weight_list=weight_list,
                               weight_percent=weight_percent, all_dates=all_dates, all_calories=all_calories,
                               burned_calorie=burned_calorie)


@app.route('/weight', methods=["GET", "POST"])
def weight():
    form = WeightForm()
    user = Users.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        new_weight = Weight(
            weight=float(form.weight.data),
            date=form.date.data,
            users_id=user.id
        )
        with app.app_context():
            db.session.add(new_weight)
            db.session.commit()
        return redirect(url_for("weight"))
    db_weight = Weight.query.filter_by(users_id=current_user.id).order_by(asc(Weight.date)).all()
    current_weight = get_weight()
    weight_loss = get_weight_loss()
    date_list = get_all_weight_dates(Weight)
    weight_list = get_all_weight()

    return render_template("weight.html", form=form, db_weight=db_weight, current_weight=current_weight,
                           weight_loss=weight_loss, date_list=date_list, current_user=current_user,
                           weight_list=weight_list)


@app.route('/food', methods=["GET", "POST"])
def food():
    form = FoodForm()
    intake_form = DateForm()
    user = Users.query.filter_by(id=current_user.id).first()
    if intake_form.submit1.data and intake_form.validate():
        get_calories()
    if form.submit.data and form.validate():
        intake_list = get_food(form.food.data)
        for i in intake_list:
            food_comp = Food(
                item=i[0],
                date=form.date.data,
                sugar=i[1],
                calories=i[2],
                meal=form.meal.data,
                food_id=user.id
            )
            with app.app_context():
                db.session.add(food_comp)
                db.session.commit()
        return redirect(url_for("food"))

    db_food = Food.query.filter_by(food_id=current_user.id).order_by(asc(Food.date)).all()
    db_intake = Intake.query.filter_by(users_id=current_user.id).order_by(asc(Intake.date)).all()
    all_calories = get_all_total_calories()
    all_sugar = get_all_total_sugar()
    all_dates = get_all_weight_dates(Intake)

    return render_template("food.html", form=form, intake_form=intake_form, current_user=current_user, db_food=db_food,
                           db_intake=db_intake, all_calories=all_calories, all_sugar=all_sugar, all_dates=all_dates)


@app.route('/exercise', methods=["GET", "POST"])
def exercise():
    form = ExerciseForm()
    exercise_date = DateForm()
    user = Users.query.filter_by(id=current_user.id).first()
    if exercise_date.submit1.data and exercise_date.validate():
        burned_calories()
    if form.submit.data and form.validate():
        workout = form.exercise.data
        workout_list = get_exercise(workout, gender=user.gender, kg=(user.s_weight / 2.2), cm=user.height, age=user.age)
        # print(workout_list)
        for i in workout_list:
            # print(i, i[0], i[1], i[2])
            workout_comp = Exercise(
                item=i[0],
                date=form.date.data,
                calories=i[2],
                exercise_id=user.id
            )
            with app.app_context():
                db.session.add(workout_comp)
                db.session.commit()
        return redirect(url_for("exercise"))
    db_exercise = Exercise.query.filter_by(exercise_id=current_user.id).order_by(asc(Exercise.date)).all()
    db_burns = Losses.query.filter_by(users_id=current_user.id).order_by(asc(Losses.date)).all()
    exercise_dict = count_exercise()
    workout_name = [key for key, value in exercise_dict.items()]
    workout_count = [value for key, value in exercise_dict.items()]
    burned_dates = get_all_weight_dates(Losses)
    burned_calorie = [cal.total_calories_loss for cal in db_burns]

    return render_template("exercise.html", form=form, current_user=current_user, exercise_date=exercise_date,
                           db_exercise=db_exercise, db_burns=db_burns, workout_name=workout_name,
                           workout_count=workout_count, burned_dates=burned_dates, burned_calorie=burned_calorie)

@app.route('/delete/<int:id>')
def delete_weight(id):
    item_to_delete = Weight.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/weight")
    except:
        return "Seem to be a problem delete that weight"

@app.route('/delete_food/<int:id>')
def delete_food(id):
    item_to_delete = Food.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/food")
    except:
        return "Seem to be a problem delete that item"

@app.route('/delete_intake/<int:id>')
def delete_intake(id):
    item_to_delete = Intake.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/food")
    except:
        return "Seem to be a problem delete that item"


@app.route('/delete_exercise/<int:id>')
def delete_exercise(id):
    item_to_delete = Exercise.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/exercise")
    except:
        return "Seem to be a problem delete that item"


@app.route('/delete_loss/<int:id>')
def delete_loss(id):
    item_to_delete = Losses.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/exercise")
    except:
        return "Seem to be a problem delete that item"


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if Users.query.filter_by(email=form.email.data).first():
            # print(Users.query.filter_by(email=form.email.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = Users(
            email=form.email.data,
            username=form.username.data,
            password=hash_and_salted_password,
            s_weight=form.s_weight.data,
            height=form.height.data,
            age=form.age.data,
            gender=form.gender.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = Sign_in()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Users.query.filter_by(username=username).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)

