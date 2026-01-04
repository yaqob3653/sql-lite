from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Account Type', choices=[('student', 'Student / Entrepreneur'), ('supplier', 'Supplier')], validators=[DataRequired()])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    description = TextAreaField('Idea Description', validators=[DataRequired()])
    submit = SubmitField('Save Idea')

class SupplierForm(FlaskForm):
    name = StringField('Supplier Name', validators=[DataRequired()])
    location = SelectField('Location', choices=[('Local', 'Local'), ('Global', 'Global')], validators=[DataRequired()])
    contact_info = StringField('Contact Info', validators=[DataRequired()])
    product_quality = SelectField('Quality', choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], validators=[DataRequired()])
    shipping_cost = StringField('Estimated Shipping Cost ($)', validators=[DataRequired()])
    taxes = StringField('Estimated Taxes ($)', validators=[DataRequired()])
    submit = SubmitField('Add Supplier')
