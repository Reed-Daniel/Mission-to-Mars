#import Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for
#PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
#import to use the scraping code so we can convert from Jupyter notebook to Python.
import scraping

#set up flask
app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#define route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#define scraping route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

#run flask
if __name__ == "__main__":
   app.run()