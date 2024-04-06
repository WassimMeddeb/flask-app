from flask import Blueprint, render_template, redirect, flash, session,request

main_routes = Blueprint("main_routes", __name__)
auth_routes = Blueprint("auth_routes", __name__)

@main_routes.route('/')
def index():
    return redirect('/login')
@main_routes.before_request
def check_logged_in():
    if 'username' not in session and request.endpoint != 'auth_routes.login':
        flash('Please log in to access this page.', 'error')
        return redirect('/login')
@main_routes.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect('/login')

@main_routes.route('/home')
def home():
    if 'username' in session:
        message = session.pop('message', None)
        username = session['username']
        return render_template('index.html', message=message, username=username)
    else:
        flash('Please log in to access this page.', 'error')
        return redirect('/login')
