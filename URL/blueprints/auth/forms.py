from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, URL


class RegistrationForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
        ],
    )
    email = StringField(
        "Email", validators=[DataRequired(), Length(min=2, max=255), Email()]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=255)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords do not match"),
        ],
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
