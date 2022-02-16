from flask import Blueprint, render_template, redirect, url_for, flash, request, session, request
from bson.objectid import ObjectId
from db import db,users
import bcrypt

routes = Blueprint("users", __name__, url_prefix="/users")


@routes.route("/")
def index():
    users = db.users.find({})
    return render_template('index.html', users=users)

# create new user
@routes.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            # hash password
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8') , bcrypt.gensalt())
            # add to db
            users.insert_one({'name': request.form['username'], 'password': hashpass})
            # create session
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'
    return render_template('new_user.html', users=users)


# user login
@routes.route('/login', methods=['POST'])
def login():
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        # checks if passwords are same
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            # add user to session
            session['username'] = request.form['username']
            flash("Login successful", "success")
        return redirect(url_for('index'))
    # if password is wrong or username doesnt exist
    return 'Invalid username/password combination'


# 
