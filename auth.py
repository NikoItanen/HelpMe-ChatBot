from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import User, dynamodb

auth_bp = Blueprint('Auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    #Create login route implementation here:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User(dynamodb.Table('UserData'))
        
        user_data = user.get_user(username)
        
        if user_data and user.check_password(user_data, password):
            session['user_id'] = user.data['username']
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
    print("Rekisteri sivulle ohjaus")
    return render_template('register.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    
    #Create register route implementation here:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_verify = request.form['password_verify']
        
        user = User(dynamodb.Table('UserData'))
        
        #Check if the username already exists
        if user.get_user(username):
            flash('Username already exists.', 'error')
            return redirect(url_for('Auth.register'))
        
        if password != password_verify:
            flash('The passwords did not match. Please try again.', 'error')
            return redirect(url_for('Auth.register'))
        
        #Create a new user
        user.put_user(username, password)
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('Auth.login'))
    
    return render_template('login.html')