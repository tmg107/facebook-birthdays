from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
# Authentication page shown here

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        # Check if user exists in db
        user = User.query.filter_by(email=email).first()
        if user:
            # If user, check if password hash is the same for user
            if check_password_hash(user.password, password):
                flash('Log-in successful!', category='success')
                # Store data for given user
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again...', category='error')
        else:
            flash('Email does not exist...', category='error')


    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    data = request.form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)

        # Check if user * already* exists in db
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        # Check if notation is correct to submit form
        elif '@' not in email:
            flash('Email does not contain correct format', category='error')
        elif len(password) == 0:
            flash('Password is empty', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user) 
            db.session.commit()
            # Store data for given user
            login_user(user, remember=True)
            flash('Account created!', category='success')  
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    # Logout the current user
    logout_user()
    return redirect(url_for('auth.login'))



