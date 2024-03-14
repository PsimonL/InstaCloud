# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    render_template,
    request
)

blueprint = Blueprint("public", __name__, static_folder="../static")


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
        return render_template("public/home.html")

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
