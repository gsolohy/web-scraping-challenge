from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri= 'mongodb://localhost:27017/mars_mission_db')

@app.route('/')
def index():
    about_mars = mongo.db.about_mars.find_one()
    return render_template("index.html", about_mars=about_mars)

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.about_mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)