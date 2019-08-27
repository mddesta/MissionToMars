    
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://<dbuser>:<dbpassword>@ds353007.mlab.com:53007/heroku_vvpt4f2t"
mongo=PyMongo(app)

@app.route("/")
def home():
    mars_info = mongo.db.mars_info.find_one()

    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_data()
    mars_info.update({}, mars_data, upsert=True)
    
    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)