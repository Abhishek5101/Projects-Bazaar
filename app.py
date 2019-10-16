from flask import Flask, render_template, url_for, flash, request, redirect
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://abhi:intensive472@intensive-lsw6x.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["Database"]
projects = db["projects"]

app = Flask(__name__)
@app.route('/')
def home():
	return render_template('home.html', projects=projects.find())


@app.route('/form', methods=["GET", "POST"])
def form():
	req = request.form
	if request.method == "POST":
		project = {
			"name": req["name"],
			"description": req["description"],
			"img_url": req["url"],
			"githuburl": req["githuburl"]
		}
		projects.insert_one(project)
	elif request.method == "GET":
		return render_template('/project_form.html')
	return redirect('/')


@app.route('/home', methods=["GET"])
def homeie():
	return render_template('home.html', projects=projects.find())
