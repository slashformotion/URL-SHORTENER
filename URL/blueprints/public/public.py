from URL.db import models, db
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
    link = models.Link.query.filter_by(shorten=shorten).first()
    base = link.base
    ip_address = request.remote_addr
    hit = models.Hit(ip=ip_address)
    db.session.add(hit)
    db.session.commit()
    ##
    #IP address is saved for later. The location can be deduced with it.
    ##
    

    return redirect(base)
