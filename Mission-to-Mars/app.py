# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping_mars
import os


# Create a Flask instance
app = Flask(__name__, image_1='/image_1')

# Set up pymongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create a route to index.html and that can find docs. from mongo
@app.route("/")
def index():
    # Declare and assign a variable to store data
    mars_data = mongo.db.mars_info.find_one()
    
    # Return data 
    return render_template("index.html", mars_info=mars_info)


# Declare route that lead to scraping
@app.route("/scrape")
def scrape():
    
    # Srape funcs
    mars_information = mongo.db.mars_information
    mars_data = scraping_mars.info()
    mars_information.update({}, mars_data, upsert=True)
    mars_weather = scraping_mars.scraping_mars_weather()

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)