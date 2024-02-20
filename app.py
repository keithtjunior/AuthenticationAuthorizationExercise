"""Feedback application."""

from flask import Flask, request, render_template, redirect, session, flash, send_from_directory
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from sqlalchemy.exc import IntegrityError
from forms import UserRegistrationForm, UserLoginForm, FeedbackCreateForm, FeedbackEditForm
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'blueoceanfloorXfrequenciessolow'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404) 
def not_found(e): 
    return render_template('error-404.html', e=e)

@app.errorhandler(401) 
def unauthorized(e): 
    return render_template('error-401.html', e=e)

@app.errorhandler(405) 
def not_allowed(e): 
    return render_template('error-405.html', e=e)

@app.route('/')
def home():
    # app.logger.info('variable: %s', variable)
    # import pdb;  pdb.set_trace()
    # records = [dict(zip(user.keys(), user)) for user in users]
    if 'is_admin' in session and session.get('is_admin') == True:
        return redirect(f'/users/{session["username"]}')
    return redirect('/register')


####################### AUTH #######################

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session and session.get('is_admin') == False:
        return redirect(f'/users/{session["username"]}')
    form = UserRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        email = form.email.data.strip()
        first_name = form.first_name.data.strip()
        last_name = form.last_name.data.strip()
        new_user = User.register(username, password, email, first_name, last_name, is_admin=False)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username is unavailable. Please pick another.')
            return render_template('register.html', form=form)
        flash('Welcome! Your account was successfully created!', "success")
        if session.get('is_admin') == True:
            return redirect(f'/users/{session["username"]}')
        else:
            session['username'] = new_user.username
            return redirect(f'/users/{new_user.username}')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(f'/users/{session["username"]}')
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        user = User.authenticate(username, password)
        if user['valid']:
            session['username'] = user['user'].username
            session['is_admin'] = user['user'].is_admin
            flash('Welcome back!', "info")
            return redirect(f'/users/{user["user"].username}')
        else:
            if user['message'] == 'username':
                form.username.errors = ['Invalid username. Please try again.']
            else:
                form.password.errors = ['Invalid password. Please try again.']
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    if session.get('is_admin') == True:
        session.pop('is_admin')
    flash('You have been logged out. Come back soon!', "info")
    return redirect('/')

####################### USER #######################

@app.route('/users/<username>')
def user_info(username):
    if 'username' not in session:
        return redirect('/')
    user = User.query.get_or_404(username)
    return render_template('user.html', user=user)

@app.route('/users/<username>/delete', methods=["POST"])
def user_delete(username):
    user = User.query.get_or_404(username)
    if ('username' not in session or username != session['username']) and ('username' not in session or session.get('is_admin') == False):
        return redirect('/')
    db.session.delete(user)
    db.session.commit()
    if not session['is_admin']:
        session.pop('username')
        session.pop('is_admin')
    flash('User was successfully deleted.', "warning")
    return redirect('/')

####################### FEEDBACK #######################

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback_add(username):
    if ('username' not in session or username != session['username']) and ('username' not in session or session.get('is_admin') == False): 
        return redirect('/')
    form = FeedbackCreateForm() 
    if form.validate_on_submit():
        title = form.title.data.strip()
        content = form.content.data.strip()
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback was successfully created.', "info")
        return redirect(f'/users/{username}')
    return render_template('add-feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def feedback_update(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if ('username' not in session or feedback.username != session['username']) and ('username' not in session or session.get('is_admin') == False):
        return redirect('/')
    form = FeedbackEditForm() 
    form.title.default = feedback.title
    if request.method == 'GET':
        form.content.data = feedback.content
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Feedback was successfully updated.', "info")
        return redirect(f'/users/{feedback.username}')
    return render_template('update-feedback.html', form=form, username=feedback.username)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def feedback_delete(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if ('username' not in session or feedback.username != session['username']) and ('username' not in session or session.get('is_admin') == False):
        return redirect('/')
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback was successfully deleted.', "warning")
    return redirect(f'/users/{feedback.username}')