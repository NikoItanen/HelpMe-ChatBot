from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import Config
from models import User
from models import db

auth_bp = Blueprint('Auth', __name__)
auth_bp.config = Config

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    #Create login route implementation here:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login Successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
        
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    #Create logout route implementation here:
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def route_register_page():
    return render_template('register.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    #Create register route implementation here:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_verify = request.form['password_verify']
        
        #Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('Auth.route_register_page'))
        
        if password != password_verify:
            flash('The passwords did not match. Please try again.', 'error')
            return redirect(url_for('Auth.route_register_page'))
        
        #Create a new user
        new_user = User(username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('Auth.login'))
    
    return redirect(url_for('Auth.route_register_page'))