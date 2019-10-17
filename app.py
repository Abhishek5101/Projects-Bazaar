from flask import Flask, render_template, url_for, flash, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

cluster = MongoClient("mongodb+srv://abhi:intensive472@intensive-lsw6x.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["Database"]
projects = db["projects"]
users = db["users"]


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


@app.route('/delete/<projectid>')
def delete(projectid):
	projects.delete_one({'_id': ObjectId(projectid)})
	return redirect('/')


@app.route('/edit/<projectid>')
def edit(projectid):
	project = projects.find_one({'_id': ObjectId(projectid)})
	return render_template('/edit_form.html', project=project)


@app.route('/edit/<projectid>', methods=["POST"])
def edit_project(projectid):
	req = request.form
	updated_project = {
			"name": req["name"],
			"description": req["description"],
			"img_url": req["url"],
			"githuburl": req["githuburl"]
		}
	projects.update_one({'_id': ObjectId(projectid)}, {'$set': updated_project})
	return redirect('/')
