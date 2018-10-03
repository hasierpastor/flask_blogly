"""Blogly application."""

from flask import Flask,request, redirect, render_template, jsonify, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
debug = DebugToolbarExtension(app)

# db.create_all()

@app.route('/')
def redirect_list_users():
    """Directs to the home page which contains a list of users"""
    return redirect('/users')


@app.route('/users')
def display_list_users():
    """Display a list of users"""
    
    #query that returns a list of tuples with the users first and last name
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('user_list.html', users=users)

@app.route('/users/new')
def add_user_form():
    """Display a form which allows you to create a new user"""
    return render_template('user_form.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():
    """Get user details from form and add user to our database, redirect to user
    list after """

    first_name = request.form.get('first-name') or None
    last_name = request.form.get("last-name") or None
    image_url = request.form.get('image-url') or None
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def display_user_details(user_id):
    """Display the users details"""

    user = User.query.get(user_id)

    return render_template('user_details.html', user=user, id=user.id)


@app.route('/users/<int:user_id>/edit')
def display_edit_user_form(user_id):
    """Display a form to edit a users details"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html',user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """On 'Save' let's update the row for the user in table"""

    user_to_edit = User.query.get_or_404(user_id)

    user_to_edit.first_name = request.form.get('first-name') or None
    user_to_edit.last_name = request.form.get("last-name") or None
    user_to_edit.image_url = request.form.get('image-url') or None


    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')