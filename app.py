# -*- coding: utf-8 -*-
"""
Created on Tue May  8 00:11:45 2018

@author: mitra
"""

from flask import Flask, render_template, jsonify, redirect
import pymongo
import Mars_scrap
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.Mars_db
collection = db.Mars_db

from flask_pymongo import PyMongo
# create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app)


@app.route("/")
def index():
    list =[]
    Mars = collection.find_one()
    return render_template("index.html", Mars=Mars)

@app.route("/scrape")
def scrape():
    Mars = mongo.db.Mars
    Mars_data = Mars_scrap.scrape()
    Mars.update(
        {},
        Mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)
    
if __name__ == "__main__":
    app.run(debug=True)
