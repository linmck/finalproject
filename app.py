# Import necessary libraries
from flask import Flask, render_template, redirect, request
# from flask_pymongo import PyMongo
# import pymongo
import predict


# Create instance of Flask app
app = Flask(__name__)


# Create routes that render the HTML templates
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/primary")
def primary():
    return render_template("primary.html")

@app.route("/secondary")
def secondary():
    return render_template("secondary.html")

@app.route("/predictor", methods=['GET', 'POST'])
def predictor():
    return render_template("predictor.html")


# Submit form to calculate model score and HDI
@app.route("/score", methods=['GET', 'POST'])
def score():

    indicators = []
    values = []

    # Form inputs
    lifeexpectancy = request.form['lifeexpectancy']
    agriculture = request.form['agriculture']
    gdp = request.form['gdp']
    gni = request.form['gni']
    population = request.form['population']

    if lifeexpectancy:
        indicator = "Life expectancy"
        indicators.append(indicator)
        values.append(lifeexpectancy)

    if agriculture:
        indicator = "Agriculture (% GDP)"
        indicators.append(indicator)
        values.append(agriculture)

    if gdp:
        indicator = "GDP per capita"
        indicators.append(indicator)
        # Convert GDP to billion
        # gdp = float(gdp) * 1000000000
        values.append(gdp)

    if gni:
        indicator = "GNI per capita"
        indicators.append(indicator)
        # Convert GNI to billion
        # gni = float(gni) * 1000000000
        values.append(gni)

    if population:
        indicator = "Population"
        indicators.append(indicator)
        # Convert population to million
        population_m = float(population) * 1000000
        values.append(population_m)

    if len(indicators) == 0:
        score = 0
        hdi = 0
    else:
        # Calculate score
        _, _, _, score, mse = predict.score_model(indicators)
        # Calculate HDI
        hdi = predict.predict_hdi(indicators, values)

        if score > 1:
            score = 1
        elif score < 0:
            score = 0

        if hdi > 1:
            hdi = 1
        elif hdi < 0:
            hdi = 0   

        # Round to 2 decimal places
        score = round(score, 2)
        hdi = round(hdi, 2)

<<<<<<< HEAD
    return render_template('predictor.html', score=score, hdi=hdi, 
        lifeexpectancy=lifeexpectancy, agriculture=agriculture, gdp=gdp, gni=gni, population=population)
=======
    if hdi > 1:
        hdi = 1
    elif hdi < 0:
        hdi = 0   

    return render_template('predictor.html', score=score, hdi=hdi)
>>>>>>> bcf2ea2fd86cf9b734ba0fd5d7ebad5f2702638b


# Preview locally on http://127.0.0.1:5000/
if __name__ == "__main__":
    app.run(debug=True)
