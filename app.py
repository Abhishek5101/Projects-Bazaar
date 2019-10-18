from flask import Flask, render_template, url_for, flash, request, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt


app = Flask(__name__)


app.config["SECRET_KEY"] = "iHpc3WXh7qzdN_JaGAQmqA"
cluster = MongoClient("mongodb+srv://abhi:intensive472@intensive-lsw6x.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["Database"]
projects = db["projects"]
users = db["users"]


@app.route('/')
def home():
	return render_template('home.html', projects=projects.find())


@app.route('/form', methods=["GET", "POST"])
def form():
	user = session['user']['username']
	req = request.form
	if request.method == "POST":
		project = {
			"name": req["name"],
			"description": req["description"],
			"img_url": req["url"],
			"githuburl": req["githuburl"],
			'creator': user
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
	project = projects.find_one({'_id': ObjectId(projectid)})
	if session:
		if project['creator'] == session['user']['username']:
			projects.delete_one({'_id': ObjectId(projectid)})
			return redirect('/')
		else:
			return '<h1> Not Owner</h1>'
	return redirect('/')


@app.route('/edit/<projectid>')
def edit(projectid):
	project = projects.find_one({'_id': ObjectId(projectid)})
	if session:
		if project['creator'] == session['user']['username']:
			return render_template('/edit_form.html', project=project)
		else:
			return '<h1>Not Owner</h1>'
	else:
		redirect('/')


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


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
	req = request.form
	if request.method == "POST":
		username = req["username"]
		password = req["password"].encode('utf-8')
		user = users.find_one({"username": username})
		# if user_exists:
		if not user and not bcrypt.checkpw(password, user['password']):
			return redirect('/sign_in')
		else:
			session.clear()
			session['user'] = {'username': user['username']}
			return redirect('/')
	elif request.method == "GET":
		return render_template('sign_in.html')
	

@app.route('/register')
def register():
	if 'user' in session:
		return render_template('register.html', user=True)
	else:
		return render_template('register.html')


@app.route('/register', methods=["POST"])
def user_register():
	"""Add a new user to mongodb database"""
	req = request.form
	encoded_pass = req['password'].encode('utf-8')
	user = {
		'username': req['username'],
		'password': bcrypt.hashpw(encoded_pass, bcrypt.gensalt())
	}
	session.clear()
	users.insert_one(user)
	session['user'] = {'username': user['username']}
	return redirect('/sign_in')


@app.route('/sign_out')
def sign_out():
	session.clear()
	print(session)
	return redirect('/')

