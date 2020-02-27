# Import necessary libraries
from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import pymongo
import predict


# Create instance of Flask app
app = Flask(__name__)


# Create routes that render the HTML templates
@app.route("/")
def index():
    return render_template("index.html")

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
    population = request.form['population']
    employment = request.form['employment']

    if lifeexpectancy:
        indicator = "Life expectancy"
        indicators.append(indicator)
        values.append(lifeexpectancy)

    if agriculture:
        indicator = "Agriculture (% GDP)"
        indicators.append(indicator)
        values.append(agriculture)

    if gdp:
        indicator = "GDP (USD)"
        indicators.append(indicator)
        values.append(gdp)

    if population:
        indicator = "Population"
        indicators.append(indicator)
        values.append(population)

    if employment:
        indicator = "Employment (%)"
        indicators.append(indicator)
        values.append(employment)

    if len(indicators) == 0:
        score = 0
        hdi = 0

    # Calculate score
    _, _, _, score, mse = predict.score_model(indicators)
    # Calculate HDI
    hdi = predict.predict_hdi(indicators, values)

    # Round to 2 decimal places
    score = round(score, 2)
    hdi = round(hdi, 2)

    return render_template('predictor.html', score=score, hdi=hdi)


# Preview locally on http://127.0.0.1:5000/
if __name__ == "__main__":
    app.run(debug=True)
