from flask import Blueprint, render_template, redirect, flash, session, request
import sqlite3
import hashlib
import hmac
import os
import secrets

auth_routes = Blueprint("auth_routes", __name__)

# Convert the HMAC_KEY string to bytes
hmac_key_str = os.getenv("HMAC_KEY")
hmac_key = b'5ba7a785971261dd8e12bceb074b1824'

# Function to generate HMAC
def generate_hmac(data):
    hmac_obj = hmac.new(hmac_key, data.encode('utf-8'), hashlib.sha256)
    return hmac_obj.hexdigest()

@auth_routes.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect('/register')

        # Generate a random key for HMAC
        key = secrets.token_hex(16)

        # Hash the password with HMAC
        hashed_password = generate_hmac(password)

        conn = sqlite3.connect('drax.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, email, password, key) VALUES (?, ?, ?, ?)",
                      (username, email, hashed_password, key))
            conn.commit()
            conn.close()
            flash('User created successfully!', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            flash('Email already exists. Please use a different email.', 'error')
            return redirect('/register')

    return render_template('register.html')

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
       
        return redirect('/home')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('drax.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()

        if user:
            stored_password = user[3]  # Assuming password is at index 3
            hashed_password = generate_hmac(password)

            if hmac.compare_digest(stored_password, hashed_password):
                session['username'] = user[1]  # Assuming username is at index 1
                flash('Logged in successfully', 'success')
                
                # Redirect to the appropriate page after successful login
                return redirect('/home')
            else:
                flash('Incorrect password. Please try again.', 'error')
                return redirect('/login')
        else:
            flash('User not found, please contact the responsible for access.', 'error')
            return redirect('/login')

    return render_template('login.html')
