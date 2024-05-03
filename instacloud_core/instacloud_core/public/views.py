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
from instacloud_core.ml_models.model import predict_class
from ..models.User import User
from ..models.UserPicture import UserPicture
import os
import tempfile
from instacloud_core.extensions import db, bcrypt, login_manager
from .s3client import S3_Client
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.utils import secure_filename
from uuid_extensions import uuid7str


login_manager.login_view = "public.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

@blueprint.route("/", methods=["GET"])
@login_required
def home():
    """Home page."""
    all_user_pics = UserPicture.query.all()
    s3_urls = []
    for user_pic in all_user_pics:
        s3_urls.append(s3_client.get_s3_url(user_pic.picture_identifier))
        
    ctx = {"s3_urls": s3_urls}
    return render_template("/public/home.html", ctx=ctx)

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

        file = request.files['file']
        if file.filename == '':
            return render_template("public/upload.html", error="No selected file")

        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file.save(tmp.name)
            try:
                # Predict class
                predicted_class = predict_class(tmp.name)
                file_identifier = uuid7str()
                if predicted_class.lower() in ['cat', 'dog']:
                    # If class is cat or dog, upload the file to S3
                    file.seek(0)
                    current_app.logger.debug(file_identifier)
                    s3_client.upload_file(file, filename_in_s3=file_identifier)

                    userPicture = UserPicture(user_id=current_user.id, picture_identifier=file_identifier, picture_tag=predicted_class.lower())
                    db.session.add(userPicture)
                    db.session.commit()
                    
                    current_app.logger.debug(userPicture)

                    return render_template("public/home.html")
                else:
                    # If class is not cat or dog, do not upload and return an error
                    return render_template("public/upload.html", error="Uploaded file is not a cat or dog")
            except Exception as ex:
                current_app.logger.error(f"Exception: {ex}")
                return render_template("public/upload.html", error="Something went wrong")
            finally:
                os.unlink(tmp.name)  # Delete the temporary file


@blueprint.route("/browse/<animal>", methods=["GET"])
@login_required
def browse(animal):
    """Browse page."""
    current_app.logger.info("Hello from the browse page!")
    user_pictures = db.session.query(UserPicture).filter(UserPicture.picture_tag == animal).order_by(UserPicture.id.desc()).limit(10).all()
    picture_urls = [s3_client.get_s3_url(user_picture.picture_identifier) for user_picture in user_pictures] 

    return render_template("public/browse.html", image_links=picture_urls, pet=animal)

@blueprint.route("/about", methods=["GET"])
def about():
    """About page."""
    current_app.logger.info("Hello from the about page!")

    return render_template("public/about.html")
