from flask import Blueprint, render_template, request, redirect, url_for, session

# Create a Blueprint for login related routes
login_bp = Blueprint('login', __name__)

# Example of user credentials (replace with your actual authentication logic)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

# Route for displaying the login form
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate user credentials (replace with your actual authentication logic)
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to the home page or another page
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

# Route for logging out
@login_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))  # Redirect to the home page or another page
