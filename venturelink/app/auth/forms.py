from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

# List of known disposable/temporary email domains
DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "10minutemail.com",
    "tempmail.com",
    "guerrillamail.com"
}


class RegistrationForm(FlaskForm):
    # Email input field with required + format validation
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Enter a valid email address.")
    ])

    # Dropdown for selecting user role
    role = SelectField(
        'I am a...',
        choices=[
            ('startup', 'Startup / Founder'),
            ('investor', 'Investor')
        ]
    )

    # Password field with minimum length requirement
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters.")
    ])

    # Confirm password must match password field
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])

    # Submit button
    submit = SubmitField('Create Account')

    # Custom email validation
    def validate_email(self, field):
        email = field.data.lower()  # Normalize email to lowercase
        domain = email.split('@')[-1]  # Extract domain

        # Block disposable email providers
        if domain in DISPOSABLE_DOMAINS:
            raise ValidationError("Disposable email addresses are not allowed.")

        # Check if email already exists in database
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError("An account with that email already exists.")

    # Custom password strength validation
    def validate_password(self, field):
        password = field.data

        # Require at least one uppercase letter
        if not any(c.isupper() for c in password):
            raise ValidationError("Password must include at least one uppercase letter.")

        # Require at least one lowercase letter
        if not any(c.islower() for c in password):
            raise ValidationError("Password must include at least one lowercase letter.")

        # Require at least one number
        if not any(c.isdigit() for c in password):
            raise ValidationError("Password must include at least one number.")

        # Require at least one special character
        if not any(not c.isalnum() for c in password):
            raise ValidationError("Password must include a special character.")

        # Block very common weak passwords
        common_passwords = {"password", "123456", "password123"}
        if password.lower() in common_passwords:
            raise ValidationError("This password is too common.")


class LoginForm(FlaskForm):
    # Email field with validation
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Enter a valid email address.")
    ])

    # Password field (only required, no strength check on login)
    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    # Submit button
    submit = SubmitField('Login')
