from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.auth import auth_bp
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect logged-in users away from register page
    if current_user.is_authenticated:
        return redirect(url_for('swipe.deck'))

    form = RegistrationForm()

    # Run validation when form is submitted
    if form.validate_on_submit():
        # Normalize email to lowercase before saving
        email = form.email.data.lower()

        # Hash password securely before storing
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        # Create new user object
        user = User(
            email=email,
            password=hashed_pw,
            role=form.role.data
        )

        # Save user to database
        db.session.add(user)
        db.session.commit()

        # Log the user in after successful registration
        login_user(user)

        # Show success message
        flash('Account created! Complete your profile to start swiping.', 'success')

        # Redirect to profile setup page
        return redirect(url_for('profiles.edit'))

    # Render registration page with form
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect already logged-in users
    if current_user.is_authenticated:
        return redirect(url_for('swipe.deck'))

    form = LoginForm()

    # Validate form submission
    if form.validate_on_submit():
        email = form.email.data.lower()  # Normalize email
        user = User.query.filter_by(email=email).first()

        # Check if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)  # Log user in
            return redirect(url_for('swipe.deck'))

        # Show error if login fails
        flash('Invalid email or password.', 'danger')

    # Render login page
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required  # Only logged-in users can access logout
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('auth.login'))  # Redirect to login page
