from flask import Blueprint, request, redirect, url_for, session, flash
from models import User, dynamodb

auth_bp = Blueprint('Auth', __name__)

@auth_bp.route('/loginHandle', methods=['GET', 'POST'])
def loginHandle():

    #Create login route implementation here:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User(dynamodb.Table('UserData'))
        
        user_data = user.get_user(username)
        
        if user_data and user.check_password(user_data, password):
            session['username'] = user_data['username']
            print(session)
            flash('Login Successful!', 'success')
            return redirect(url_for('Routes.index'))
        else:
            flash('Invalid username or password.', 'error')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    #Create logout route implementation here:
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('Routes.index'))

@auth_bp.route('/registerHandle', methods=['GET', 'POST'])
def registerHandle():
    print("login toimii")
    #Create register route implementation here:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_verify = request.form['password-verify']
        
        user = User(dynamodb.Table('UserData'))
        
        #Check if the username already exists
        if user.get_user(username):
            flash('Username already exists.', 'error')
            return redirect(url_for('Routes.register'))
        
        if password != password_verify:
            flash('The passwords did not match. Please try again.', 'error')
            return redirect(url_for('Routes.register'))
        
        #Create a new user
        user.put_user(username, password)
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('Routes.login'))