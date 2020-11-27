from URL.db import models
from flask import Blueprint, request, redirect, url_for, render_template


public_bp = Blueprint("public", __name__, template_folder="templates")


@public_bp.route("/")
def index():

    return render_template("public/index.html")


@public_bp.route("/about")
def about():
    return "about"


@public_bp.route("/r/<string:shorten>/")
def redirection(shorten):
    print("shorten",shorten)
    link = models.Link.query.filter_by(shorten=shorten).first()
    print('link', link)
    base = link.base
    a=1

    return redirect(base)
