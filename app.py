# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import predict

# create instance of Flask app
app = Flask(__name__)

# Create connection variable
# conn = 'mongodb://localhost:27017'
mongo = PyMongo(app, uri="mongodb://localhost:27017/hdi_db")
# mongo = PyMongo(app, uri="mongodb://heroku_hv2f4db0:p9870ic6bh2r4flii7fdvd8rn0@ds155596.mlab.com:55596/heroku_hv2f4db0")

# Pass connection to the pymongo instance.
# client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
# db = client.hdi_db

# Drops collection if available to remove duplicates
# db.models.drop()

# Creates a collection in the database
mongo.db.models.insert_many(
    [
        {
            "score": "0.83",
            "hdi": "0.60"
        },
        {
            "score": "0.30",
            "hdi": "0.50"
        }
    ]
)

# create routes that renders the HTML templates
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predictor")
def predictor():
    scores = list(mongo.db.models.find({"score": "0.30"}))
    model = scores[0]
    return render_template('predictor.html', output=model)

@app.route("/predictor2")
def predictor2():
    scores = list(mongo.db.models.find({"score": "0.83"}))
    model = scores[0]
    return render_template('predictor2.html', output=model)

@app.route("/score")
def score():
    # score = list(db.output.find())
    # return redirect("/predictor", code=302, score=score)
    pass


# Preview locally on http://127.0.0.1:5000/
if __name__ == "__main__":
    app.run(debug=True)
