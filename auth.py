from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('Auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    #Create login route implementation here:
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error='Invalid username')
    return render_template('login.html', error=None)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
     #Create logout route implementation here:
     session.pop('username', None)
     return redirect(url_for('Auth.login'))