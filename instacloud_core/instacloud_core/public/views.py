# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    url_for,
    redirect
)

from instacloud_core.extensions import db, bcrypt, login_manager
from .s3client import S3_Client
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

login_manager.login_view = "public.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

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

blueprint = Blueprint("public", __name__, static_folder="../static")
s3_client = S3_Client()

@blueprint.route("/", methods=["GET"])
@login_required
def home():
    """Home page."""
    current_app.logger.info("Hello from the home page!")
    return render_template("/public/home.html")

@blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("public.home"))
    return render_template("/authorization/login.html", form=form, error="Invalid username or password!")

@blueprint.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("public.home"))


@blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('public.login'))
    
    return render_template("/authorization/register.html", form=form)

@blueprint.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    """Upload page."""
    current_app.logger.info("Hello from the upload page!")

    if request.method == "GET":
        return render_template("public/upload.html")
    else:
        if 'file' not in request.files:
            return render_template("public/upload.html", error="No file part")
        try:
            file = request.files['file']
            if file.filename == '':
                return render_template("public/upload.html", error="No selected file")
            
            # current_app.logger.error(f"Sending file: {file}")

            s3_client.upload_file(file, filename_in_s3=file.filename)
            return render_template("public/home.html")
        except Exception as ex:
            current_app.logger.error(f"Exception: {ex}")
            return render_template("public/upload.html", error="Something went wrong")


@blueprint.route("/browse/<animal>", methods=["GET"])
@login_required
def browse(animal):
    """Browse page."""
    current_app.logger.info("Hello from the browse page!")

    return render_template("public/browse.html", pet=animal)

@blueprint.route("/about", methods=["GET"])
def about():
    """About page."""
    current_app.logger.info("Hello from the about page!")

    return render_template("public/about.html")
