# -*- coding: utf-8 -*-
"""Public forms."""

from flask_wtf.form import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms import StringField, PasswordField, SubmitField
from ..models.User import User

class RegistrationForm(FlaskForm):
    username = StringField(
                    validators=[InputRequired(), Length(min=4, max=20)], 
                    render_kw={"placeholder": "Username"}
                )
    password = PasswordField(
                    validators=[InputRequired(), Length(min=4, max=20)], 
                    render_kw={"placeholder": "Password"}
                )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_name = User.query.filter_by(
            username=username.data).first()
        if existing_user_name:
            raise ValidationError("Username already exists!")

class LoginForm(FlaskForm):
    username = StringField(
                    validators=[InputRequired(), Length(min=4, max=20)], 
                    render_kw={"placeholder": "Username"}
                )
    password = PasswordField(
                    validators=[InputRequired(), Length(min=4, max=20)], 
                    render_kw={"placeholder": "Password"}
                )
    submit = SubmitField("Login")