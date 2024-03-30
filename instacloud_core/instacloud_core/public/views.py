# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    render_template,
    request
)
from .s3client import S3_Client

blueprint = Blueprint("public", __name__, static_folder="../static")
s3_client = S3_Client()

@blueprint.route("/", methods=["GET"])
def home():
    """Home page."""
    current_app.logger.info("Hello from the home page!")

    return render_template("public/home.html")

@blueprint.route("/upload", methods=["POST", "GET"])
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
            
            current_app.logger.error(f"Sending file: {file}")

            s3_client.upload_file(file, filename_in_s3=file.filename)
            return render_template("public/home.html")
        except Exception as ex:
            current_app.logger.error(f"Exception: {ex}")
            return render_template("public/upload.html", error="Something went wrong")

@blueprint.route("/browse/<animal>", methods=["GET"])
def browse(animal):
    """Browse page."""
    current_app.logger.info("Hello from the browse page!")

    return render_template("public/browse.html", pet=animal)

@blueprint.route("/about", methods=["GET"])
def about():
    """About page."""
    current_app.logger.info("Hello from the about page!")

    return render_template("public/about.html")
