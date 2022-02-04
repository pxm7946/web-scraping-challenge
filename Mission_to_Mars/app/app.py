from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from scrape_mars import scrape_all

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo= PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():
    mars_data = scrape_all()
    mongo.db.collection.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
