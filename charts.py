from pychartjs import BaseChart, ChartType, Color, Options
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from sqlalchemy import true

app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Flask-Bootstrap requires this line
Bootstrap(app)

class MyBarGraph(BaseChart):

    type = ChartType.Line

    class data:
        label = "Numbers"
        data = [12, 19, 6, 17, 10]
        backgroundColor = Color.Green
        borderColor = 'rgb(75, 192, 192)'


class MyChart(BaseChart):
    type = ChartType.Bar

    class labels:
        group = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    class data:
        class apples:
            data = [2, 8, 11, 7, 2, 4, 3]
            backgroundColor = Color.Palette(Color.Hex('#30EE8090'), 7, 'lightness')
            borderColor = Color.Green
            fill = False
            yAxisID = 'apples'

        class totalEnergy:
            label = "Total Daily Energy Consumption (kJ)"
            type = ChartType.Line
            data = [5665, 5612, 7566, 8763, 5176, 5751, 6546]
            backgroundColor = Color.RGBA(0, 0, 0, 0)
            borderColor = Color.Purple
            yAxisID = 'totalenergy'

    class options:
        title = Options.Title("Apples I've eaten compared to total daily energy")

        scales = {
            "yAxes": [
                {"id": "apples",
                 "ticks": {
                     "beginAtZero": True,
                     "callback": "<<function(value, index, values) {return value + ' Big Ones';}>>",
                 }
                 },
                {"id": "totalenergy",
                 "position": "right",
                 "ticks": {"beginAtZero": True}
                 }
            ]
        }

class NewChart(BaseChart):

    type = ChartType.Line

    class labels:
        Years = list(range(2017, 2023))

    class data:
        class Whales:
            data = [80, 60, 100, 80, 90, 50]

            borderColor = Color.Purple
            fill = False
            pointBorderWidth = 5
            pointRadius = 1

        class Bears:
            data = [60, 50, 80, 120, 140, 180]
            borderColor = Color.Red
            fill = False
            pointBorderWidth = 10
            pointRadius = 3

        class Dolphins:
            data = [150, 80, 60, 30, 50, 30]
            borderColor = Color.Yellow
            fill = False
            pointBorderWidth = 10
            pointRadius = 3

    class options:

        title   = Options.Title(text="Wildlife Populations", fontSize=18)
        #
        _lables = Options.Legend_Labels(fontColor=Color.Gray, fullWidth=True)
        legend  = Options.Legend(labels=_lables)
        #
        _yAxes = [Options.General(ticks=Options.General(beginAtZero=True, padding=15, max=200))]
        #
        scales = Options.General(yAxes=_yAxes)

nine = [5665, 5612, 7566, 8763, 5176, 5751, 6546]
@app.route('/')
def home():
    new_chart = NewChart()

    ChartJSON = new_chart.get()

    return render_template("testing.html", chartJSON=ChartJSON)

@app.route('/weight', methods=["GET", "POST"])
def weight():
    form = WeightForm()

    if form.validate_on_submit():
        new_weight = Weight(
            weight=float(form.weight.data),
            date=time
        )
        with app.app_context():
            db.session.add(new_weight)
            db.session.commit()
        return redirect(url_for("food"))

    db_weight = Weight.query.all()
    current_weight = get_weight()
    weight_loss = get_weight_loss()
    date_list = get_weight_dates()
    chart_data = {
        "labels": date_list
    }

    return render_template("weight.html", form=form, db_weight=db_weight, current_weight=current_weight,
                           weight_loss=weight_loss, date_list=date_list, chart_data=chart_data)


@app.route('/food', methods=["GET", "POST"])
def food():
    form = FoodForm()

    if form.validate_on_submit():
        intake_list = get_food(form.food.data)
        for i in intake_list:
            food_comp = Food(
                item=i[0],
                date=time,
                sugar=i[1],
                calories=i[2],
                meal=form.meal.data
            )
            with app.app_context():
                db.session.add(food_comp)
                db.session.commit()
        return redirect(url_for("exercise"))
    return render_template("food.html", form=form)


@app.route('/exercise', methods=["GET", "POST"])
def exercise():
    form = ExerciseForm()

    if form.validate_on_submit():
        workout = form.exercise.data
        workout_list = get_exercise(workout, gender='male', kg=(240 / 2.2), cm=167.64, age=40)
        print(workout_list)
        for i in workout_list:
            print(i, i[0], i[1], i[2])
            workout_comp = Exercise(
                item=i[0],
                date=time,
                calories=i[2]
            )
            with app.app_context():
                db.session.add(workout_comp)
                db.session.commit()
        return redirect(url_for("home"))
    return render_template("exercise.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)