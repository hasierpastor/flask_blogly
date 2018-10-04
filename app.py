"""Blogly application."""

from flask import Flask,request, redirect, render_template, jsonify, session
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
debug = DebugToolbarExtension(app)

db.create_all()

@app.route('/')
def display_home():
    """Displays 5 most recent posts"""
    posts = Post.query.order_by(Post.created_at).limit(5).all() or []

    return render_template('home.html', posts=posts)

#user routes


@app.route('/users')
def display_list_users():
    """Display a list of users"""
    
    #query that returns a list of tuples with the users first and last name
    users = User.query.order_by(User.last_name, User.first_name).all() or []

    return render_template('user_list.html', users=users)

@app.route('/users/new')
def add_user_form():
    """Display a form which allows you to create a new user"""
    return render_template('add_user.html')

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


#switching to post routes


@app.route('/users/<int:user_id>/posts/new')
def display_post_form(user_id):
    """Show a form for a user to add a post"""

    user = User.query.get_or_404(user_id)

    tags = Tag.query.all() or []

    return render_template('add_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Add post from user and redirect to user details page"""

    post_title = request.form.get('post-title') or None
    post_content = request.form.get("post-content") or None

    new_post = Post(title=post_title, content=post_content, user_id=user_id)

    tags = request.form.getlist('tag-name')
    for tag_id in tags:
        print(tag_id)
        new_tag = Tag.query.get(tag_id)
        new_post.tags.append(new_tag)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{str(user_id)}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post with post_id supplied"""

    post = Post.query.get(post_id) or None

    return render_template('show_post.html', post=post, user=post.user)

@app.route('/posts/<int:post_id>/edit')
def display_edit_post_form(post_id):
    """Display form to edit a post"""

    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = Tag.query.all() or []

    return render_template('edit_post.html', post=post, user=user, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """When 'Edit' is clicked, grab form data and update post in database"""

    post_to_edit = Post.query.get_or_404(post_id)

    post_to_edit.title = request.form.get('edit-title') or None
    post_to_edit.content = request.form.get("edit-content") or None

    tags = request.form.getlist('tag-name')
    new_tags = []
    for tag_id in tags:
        new_tag = Tag.query.get(tag_id)
        new_tags.append(new_tag)

    post_to_edit.tags = new_tags
    
    db.session.add(post_to_edit)
    db.session.commit()

    return redirect(f'/posts/{str(post_id)}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """When 'delete' button is clicked, remove post from database"""

    post_to_delete = Post.query.get_or_404(post_id)

    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect('/')

#switching to tag names

@app.route('/tags')
def display_tags():
    """route to a template that displays a list of all tags"""

    tags = Tag.query.all() or []

    return render_template('tag_list.html',tags=tags)

@app.route('/tags/<int:tag_id>')
def display_posts_with_tag(tag_id):
    """Displays a list of posts which have the tag id"""

    tag = Tag.query.get_or_404(tag_id) 
    posts = tag.posts

    return render_template('tag_posts_list.html', posts=posts, tag=tag)


@app.route('/tags/new')
def display_form_create_tag():
    """Display a form to create a tag"""

    return render_template('add_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
    """Takes in form data and creates a tag in the database"""

    tag_name = request.form.get('tag-name') or None

    tag = Tag(name=tag_name)
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def display_tag_edit_form(tag_id):
    """Displays a form to edit a tag"""
    
    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Takes in form data and updates a tag name in the database"""
    
    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form.get('edit-tag-name') or None
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Deletes tag from database when delete button is clicked on tag posts list page"""
    
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')