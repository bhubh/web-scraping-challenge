from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#create a mars_collection in database in mongodb
mars_collection = mongo.db.collection

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mars_collection.find_one()

    # Return template and data
    return render_template("index.html", mars = mars_data)


# set our path to /scrape
@app.route("/scrape")
def scraper():
    # call the scrape function in our scrape_mars file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape()
    # update our listings with the data that is being scraped or create&insert if collection doesn't exist
    mars_collection.update_one({}, {"$set": mars_data}, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
